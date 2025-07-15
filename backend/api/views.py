# # # from django.shortcuts import render

# # # # Create your views here.
# # # # from django.shortcuts import render

# # # # # Create your views here.
# # # # from rest_framework.views import APIView
# # # # from rest_framework.response import Response
# # # # from rest_framework import status
# # # # from .models import Prediction
# # # # from .serializers import PredictionSerializer
# # # # from .ml import classifier

# # # # class PredictView(APIView):
# # # #     def post(self, request, format=None):
# # # #         file = request.FILES.get("image")
# # # #         if not file:
# # # #             return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

# # # #         prediction_data = classifier.predict(file)

# # # #         # Save record
# # # #         prediction = Prediction.objects.create(
# # # #             image=file,
# # # #             color=prediction_data["color"],
# # # #             pattern=prediction_data["pattern"],
# # # #             category=prediction_data["category"],
# # # #             sleeve=prediction_data["sleeve"],
# # # #             neckline=prediction_data["neckline"],
# # # #             fit=prediction_data["fit"],
# # # #             occasion=prediction_data["occasion"],
# # # #             material=prediction_data["material"],
# # # #             confidence=prediction_data["confidence"],
# # # #         )
# # # #         serializer = PredictionSerializer(prediction)
# # # #         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from .ml import FashionClassifier
# # # import os

# # # classifier = FashionClassifier()

# # # class PredictView(APIView):
# # #     def post(self, request, format=None):
# # #         file = request.FILES.get("image")
# # #         if not file:
# # #             return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

# # #         # Save uploaded file
# # #         upload_dir = "media/uploads"
# # #         os.makedirs(upload_dir, exist_ok=True)
# # #         file_path = os.path.join(upload_dir, file.name)

# # #         with open(file_path, "wb+") as f:
# # #             for chunk in file.chunks():
# # #                 f.write(chunk)

# # #         # Get dummy prediction
# # #         prediction, json_path = classifier.predict(file_path)

# # #         return Response({
# # #             "message": "Prediction successful",
# # #             "prediction": prediction,
# # #             "json_file": json_path
# # #         }, status=status.HTTP_200_OK)


# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from .ml import FashionClassifier
# # import os

# # from rest_framework.views import APIView
# # from rest_framework.response import Response

# # class SessionPredictionsView(APIView):
# #     def get(self, request, format=None):
# #         predictions = request.session.get("predictions", [])
# #         return Response({"predictions": predictions})


# # classifier = FashionClassifier()

# # class PredictView(APIView):
# #     def post(self, request, format=None):
# #         file = request.FILES.get("image")
# #         if not file:
# #             return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

# #         upload_dir = "media/uploads"
# #         os.makedirs(upload_dir, exist_ok=True)
# #         file_path = os.path.join(upload_dir, file.name)

# #         with open(file_path, "wb+") as f:
# #             for chunk in file.chunks():
# #                 f.write(chunk)

# #         prediction, json_path = classifier.predict(file_path)

# #         return Response({
# #             "message": "Prediction successful",
# #             "prediction": prediction,
# #             "json_file": json_path,
# #         }, status=status.HTTP_200_OK)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .ml import FashionClassifier
# import os

# classifier = FashionClassifier()

# class PredictView(APIView):
#     def post(self, request, format=None):
#         files = request.FILES.getlist("images")
#         if not files:
#             return Response({"error": "No images uploaded"}, status=status.HTTP_400_BAD_REQUEST)

#         # Make sure session exists
#         session_id = request.session.session_key
#         if not session_id:
#             request.session.create()
#             session_id = request.session.session_key

#         upload_dir = os.path.join("media/uploads", session_id)
#         os.makedirs(upload_dir, exist_ok=True)

#         # Load existing predictions for this session
#         session_predictions = request.session.get("predictions", [])

#         new_predictions = []

#         for file in files:
#             file_path = os.path.join(upload_dir, file.name)
#             with open(file_path, "wb+") as f:
#                 for chunk in file.chunks():
#                     f.write(chunk)

#             prediction, json_path = classifier.predict(file_path)

#             record = {
#                 "filename": file.name,
#                 "filepath": f"uploads/{session_id}/{file.name}",
#                 "prediction": prediction,
#                 "json_file": json_path,
#             }
#             new_predictions.append(record)
#             session_predictions.append(record)

#         # Save updated list back to session
#         request.session["predictions"] = session_predictions

#         return Response({
#             "message": "Predictions successful",
#             "predictions": new_predictions,
#         }, status=status.HTTP_200_OK)


# class SessionPredictionsView(APIView):
#     def get(self, request, format=None):
#         predictions = request.session.get("predictions", [])
#         return Response({"predictions": predictions})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

class PredictView(APIView):
    def post(self, request, format=None):
        # Lazy import FashionClassifier
        from .ml import FashionClassifier

        files = request.FILES.getlist("images")
        if not files:
            return Response({"error": "No images uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure session exists
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        upload_dir = os.path.join("media/uploads", session_id)
        os.makedirs(upload_dir, exist_ok=True)

        # Load existing predictions for this session
        session_predictions = request.session.get("predictions", [])

        new_predictions = []

        # Create classifier here
        classifier = FashionClassifier()

        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            prediction, json_path = classifier.predict(file_path)

            record = {
                "filename": file.name,
                "filepath": f"uploads/{session_id}/{file.name}",
                "prediction": prediction,
                "json_file": json_path,
            }
            new_predictions.append(record)
            session_predictions.append(record)

        # Save updated list back to session
        request.session["predictions"] = session_predictions

        return Response({
            "message": "Predictions successful",
            "predictions": new_predictions,
        }, status=status.HTTP_200_OK)


class SessionPredictionsView(APIView):
    def get(self, request, format=None):
        predictions = request.session.get("predictions", [])
        return Response({"predictions": predictions})
