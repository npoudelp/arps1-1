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
    RecomendCrop,
    AddPlantation,
    GetPlantation,
    AddFertilizer,
    GetFertilizer,
    AddPestControl,
    GetPestControl,
    AddIrrigation,
    GetIrrigation,
    AddHarvest,
    GetHarvest,
    GetAllFieldActivities,
    ScrapeData,
    GetPinnedLocation,
    SetPinnedLocation,

    DeleteAllFrequentQuestions,
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

    # plantation
    path('plantation/add/', AddPlantation.as_view(), name='add_plantation'),
    path('plantation/get/<int:id>/', GetPlantation.as_view(), name='get_plantation'),

    # fertilizer
    path('fertilizer/add/', AddFertilizer.as_view(), name='add_fertilizer'),
    path('fertilizer/get/<int:id>/', GetFertilizer.as_view(), name='get_fertilizer'),

    # pest control
    path('pest-control/add/', AddPestControl.as_view(), name='add_pest_control'),
    path('pest-control/get/<int:id>/', GetPestControl.as_view(), name='get_pest_control'),

    # irrigation
    path('irrigation/add/', AddIrrigation.as_view(), name='add_irrigation'),
    path('irrigation/get/<int:id>/', GetIrrigation.as_view(), name='get_irrigation'),

    # harvest
    path('harvest/add/', AddHarvest.as_view(), name='add_harvest'),
    path('harvest/get/<int:id>/', GetHarvest.as_view(), name='get_harvest'),
    
    # get all field activities
    path('field-activities/all/<int:id>/', GetAllFieldActivities.as_view(), name='get_all_field_activities'),

    # scrape data
    path('scrape/<str:location>/', ScrapeData.as_view(), name='scrape_data'),

    # pinned location
    path('pinned-location/get/', GetPinnedLocation.as_view(), name='get_pinned_location'),
    path('pinned-location/add/', SetPinnedLocation.as_view(), name='set_pinned_location'),

    # delete answers #############for development and test purpose only
    path('frequent-questions/delete/', DeleteAllFrequentQuestions.as_view(), name='delete_all_frequent_questions')
]