import os
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
from PIL import Image
import json
import pandas as pd

# IMPORTANT: define BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This points to your "backend/" directory

class ModelPredictor:
    def __init__(self):
        # Load lookup data
        cat_attrs = pd.read_parquet(os.path.join(BASE_DIR, "category_attributes.parquet"))
        self.cat2N = dict(zip(cat_attrs.Category, cat_attrs.No_of_attribute))
        self.category_slot_to_attr = {}
        for _, row in cat_attrs.iterrows():
            cat = row["Category"]
            N = int(row["No_of_attribute"])
            attrs = list(row["Attribute_list"])
            slot_map = {j: attrs[j-1] for j in range(1, N+1)}
            self.category_slot_to_attr[cat] = slot_map

        with open(os.path.join(BASE_DIR, "category_slot_to_labels.json")) as f:
            self.category_slot_to_labels = json.load(f)
        self.category_slot_to_labels = {
            cat: {int(j): set(labels) for j, labels in slots.items()}
            for cat, slots in self.category_slot_to_labels.items()
        }

        with open(os.path.join(BASE_DIR, "label2idx.json")) as f:
            label2idx = json.load(f)
        self.label2idx = {int(k): v for k, v in label2idx.items()}

        mean = [0.485, 0.456, 0.406]
        std  = [0.229, 0.224, 0.225]
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.backbone = torchvision.models.efficientnet_b0(
            weights=torchvision.models.EfficientNet_B0_Weights.DEFAULT
        )
        self.backbone.classifier = nn.Identity()
        feature_dim = 1280

        self.heads = nn.ModuleList([
            nn.Linear(feature_dim, len(self.label2idx[j]))
            for j in range(1,11)
        ])

        ckpt = torch.load(os.path.join(BASE_DIR, "best_model.pth"), map_location=self.device, weights_only=False)
        self.backbone.load_state_dict(ckpt["backbone"])
        self.heads.load_state_dict(ckpt["heads"])

        self.backbone.to(self.device).eval()
        self.heads.to(self.device).eval()

    def infer_category(self, pred_labels):
        scores = {}
        for cat, N in self.cat2N.items():
            count = 0
            for j in range(1, N+1):
                pred_label = pred_labels[j-1]
                if pred_label in self.category_slot_to_labels[cat][j]:
                    count += 1
            scores[cat] = count
        best_cat = max(scores, key=scores.get)
        return best_cat

    def predict_image(self, image_path):
        img = Image.open(image_path).convert("RGB")
        x = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            feats = self.backbone(x)
            pred_labels = []
            for j in range(1, 11):
                logits = self.heads[j - 1](feats)
                pred_idx = logits.argmax(dim=1).item()
                label = [k for k, v in self.label2idx[j].items() if v == pred_idx][0]
                pred_labels.append(label)

            pred_cat = self.infer_category(pred_labels)

            # Only relevant attributes
            N = self.cat2N[pred_cat]
            relevant_attrs = {}
            for j in range(1, N + 1):
                attr_name = self.category_slot_to_attr[pred_cat][j]
                relevant_attrs[attr_name] = pred_labels[j - 1]

            # All slots for reference
            all_slots = {}
            for j in range(1, 11):
                all_slots[f"Slot_{j}"] = pred_labels[j - 1]

        return {
            "category": pred_cat,
            "attributes": relevant_attrs,
            "all_slots": all_slots
        }
