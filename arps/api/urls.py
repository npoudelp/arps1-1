from django.urls import path
from .apis import (
    AddField,
    GetField,
    UpdateField,
    GetFieldById,
    GetGeminiResponse,
    AddFrequentQuestion,
    GetFrequentQuestions,
    DeleteField,
    RecomendCrop
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # fields relates url
    path('field/add/', AddField.as_view(), name='add_field'),
    path('field/get/', GetField.as_view(), name='get_field'),
    path('field/update/<int:id>/', UpdateField.as_view(), name='update_field'),
    path('field/get/id/<int:id>/', GetFieldById.as_view(), name='get_field_by_id'),
    path('field/delete/<int:id>/', DeleteField.as_view(), name='delete_field'),
    
    # gemini url
    path('assistance/', GetGeminiResponse.as_view(), name='get_gemini_response'),

    # frequent questions url
    path('frequent-questions/add/', AddFrequentQuestion.as_view(), name='add_frequent_question'),
    path('frequent-questions/get/', GetFrequentQuestions.as_view(), name='get_frequent_questions'),

    # recomend crop
    path('recomend-crop/', RecomendCrop.as_view(), name='recomend_crop'),
]