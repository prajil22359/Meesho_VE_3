from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Prediction
# from .serializers import PredictionSerializer
# from .ml import classifier

# class PredictView(APIView):
#     def post(self, request, format=None):
#         file = request.FILES.get("image")
#         if not file:
#             return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

#         prediction_data = classifier.predict(file)

#         # Save record
#         prediction = Prediction.objects.create(
#             image=file,
#             color=prediction_data["color"],
#             pattern=prediction_data["pattern"],
#             category=prediction_data["category"],
#             sleeve=prediction_data["sleeve"],
#             neckline=prediction_data["neckline"],
#             fit=prediction_data["fit"],
#             occasion=prediction_data["occasion"],
#             material=prediction_data["material"],
#             confidence=prediction_data["confidence"],
#         )
#         serializer = PredictionSerializer(prediction)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml import FashionClassifier
import os

classifier = FashionClassifier()

class PredictView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get("image")
        if not file:
            return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded file
        upload_dir = "media/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.name)

        with open(file_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Get dummy prediction
        prediction, json_path = classifier.predict(file_path)

        return Response({
            "message": "Prediction successful",
            "prediction": prediction,
            "json_file": json_path
        }, status=status.HTTP_200_OK)
