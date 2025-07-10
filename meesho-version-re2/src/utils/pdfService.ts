import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { PredictionResult } from "@/types/prediction";

/**
 * Convert image URL to Base64
 */
function getImageDataUrl(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = function () {
      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");
      ctx?.drawImage(img, 0, 0);
      const dataURL = canvas.toDataURL("image/png");
      resolve(dataURL);
    };
    img.onerror = function () {
      reject(new Error("Failed to load image for PDF"));
    };
    img.src = url;
  });
}

export async function downloadPDF(predictions: PredictionResult[]) {
  const doc = new jsPDF();

  for (let index = 0; index < predictions.length; index++) {
    const prediction = predictions[index];

    if (index > 0) {
      doc.addPage();
    }

    // HEADER BAR
    doc.setFillColor("#e01171");
    doc.rect(0, 0, 210, 20, "F");
    doc.setFontSize(16);
    doc.setTextColor("#ffffff");
    doc.text(`Fashion Attribute Report`, 105, 13, { align: "center" });

    // CATEGORY
    doc.setFontSize(14);
    doc.setTextColor("#333333");
    doc.text(`Category:`, 14, 30);

    doc.setFontSize(14);
    doc.setTextColor("#e01171");
    doc.text(`${prediction.category}`, 42, 30);

    // IMAGE
    let imgY = 38;
    try {
      const imgData = await getImageDataUrl(prediction.imageUrl);

      const img = new Image();
      img.src = prediction.imageUrl;

      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
      });

      const imgWidth = img.width;
      const imgHeight = img.height;

      const maxWidth = 80;
      const displayWidth = Math.min(imgWidth * 0.2, maxWidth);
      const displayHeight = (imgHeight / imgWidth) * displayWidth;
      const x = (210 - displayWidth) / 2;

      doc.addImage(imgData, "PNG", x, imgY, displayWidth, displayHeight);

      imgY += displayHeight + 10;
    } catch (error) {
      console.error("Image loading failed:", error);
      doc.setFontSize(10);
      doc.setTextColor("#ef4444");
      doc.text("Image not available", 14, imgY);
      imgY += 10;
    }

    // ATTRIBUTES TABLE
    const rows = Object.entries(prediction.attributes).map(([key, value]) => [
      key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
      value && value !== "default" ? value : "Default",
    ]);

    autoTable(doc, {
      startY: imgY,
      head: [["Attribute", "Value"]],
      body: rows,
      theme: "striped",
      styles: {
        fontSize: 11,
        textColor: "#333333",
        cellPadding: 3,
      },
      headStyles: {
        fillColor: [224, 17, 113], // Meesho Pink
        textColor: "#ffffff",
        fontStyle: "bold",
      },
      alternateRowStyles: {
        fillColor: "#f7d3e8",
      },
      margin: { top: 10 },
    });

    // FOOTER
    doc.setFontSize(10);
    doc.setTextColor("#666666");
    doc.text(`Page ${index + 1} of ${predictions.length}`, 200, 290, { align: "right" });
  }

  doc.save("predictions.pdf");
}
