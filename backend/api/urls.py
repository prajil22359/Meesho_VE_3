from django.urls import path
from .views import PredictView, SessionPredictionsView

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('session-predictions/', SessionPredictionsView.as_view(), name='session_predictions'),
]
