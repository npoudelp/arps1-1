from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .gemini import ask_gemini
from .models import (
    Fields,
    FrequentQuestions,
    Plantation,
    FertilizerAddition,
    PestControl,
    Irrigation,
    Harvest,
    PinnedLocation,
    )
from .serializers import (
    FieldsSerializer,
    FrequentQuestionsSerializer,
    PlantationSerializer,
    FertilizerAdditionSerializer,
    PestControlSerializer,
    IrrigationSerializer,
    HarvestSerializer,
    PinnedLocationSerializer,

)
from .recomend import recomendCrop
from . import scrape


class AddField(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FieldsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.harvested = True
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class GetField(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        fields = Fields.objects.all().order_by('id')
        serializer = FieldsSerializer(fields, many=True)
        return Response(serializer.data, status=200)
    

# update field data
class UpdateField(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            checkHarvestedStatus = Fields.objects.get(id=id)
            if checkHarvestedStatus.harvested == False:
                return Response({"error": "Field not harvested, harvest it to change the crop"}, status=400)
            field = Fields.objects.get(id=id)
            if not request.data.get("coordinates"):
                coordinates = field.coordinates
                request.data['coordinates'] = coordinates
                
            serializer = FieldsSerializer(instance=field, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Fields.DoesNotExist:
            return Response({"error": "Field not found"}, status=404)
        
        
# get field data by id
class GetFieldById(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            field = Fields.objects.get(id=id)
            serializer = FieldsSerializer(field)
            return Response(serializer.data, status=200)
        except Fields.DoesNotExist:
            return Response({"error": "Field not found"}, status=404)
        

#delete field data
class DeleteField(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            field = Fields.objects.get(id=id)
            if field.harvested == False:
                return Response({"error": "Field not harvested, harvest it to delete"}, status=400)
            field.delete()
            return Response({"message": "Field deleted"}, status=204)
        except Fields.DoesNotExist:
            return Response({"error": "Field not found"}, status=404)



#  get gemini response
class GetGeminiResponse(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question = request.data.get("question")
        if question == "":
            return Response({"error": "Question not provided"}, status=400)
        try:
            try:
                searchQuestion = FrequentQuestions.objects.get(question=question)
                searchSerialized = FrequentQuestionsSerializer(searchQuestion)
                return Response({
                    "newquestion": False,
                    "response": searchSerialized.data["answer"],
                    "question": searchSerialized.data["question"]
                }, status=200)
            except:
                try:
                    response = ask_gemini(question)
                    return Response({
                        "newquestion": True,
                        "response": response,
                        "question": question
                    }, status=200)
                except Exception as e:
                    return Response({"error": e}, status=400)            
        except:
            return Response({"error": "Question not recognised"}, status=400)
        

# add frequent questions
class AddFrequentQuestion(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FrequentQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# get frequent questions
class GetFrequentQuestions(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        questions = FrequentQuestions.objects.all().order_by('-id')
        serializer = FrequentQuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=200)
    

#get prediction
class RecomendCrop(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        id = request.data.get("id")
        district = request.data.get("district")
        if id is None or district is None:
            return Response({"error": "Data not provided"}, status=400)
        try:
            getNPK = Fields.objects.get(id=id)
            N = getNPK.nitrogen
            P = getNPK.phosphorus
            K = getNPK.potassium
            ph = getNPK.ph

            if N is None or P is None or K is None or ph is None or ph == 0 or district is None:
                return Response({"error": "Data not provided or not availabale, check fields"}, status=400)

            crops = recomendCrop(N, P, K, ph, district)
            return Response({
                "crops": crops
            }, status=200)

        except:
            return Response({"error": "Prediction failed"}, status=400)
        

# add plantation info
class AddPlantation(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = PlantationSerializer(data=request.data)
            if serializer.is_valid():
                fieldId = request.data.get("field")
                checkField = Fields.objects.get(id=fieldId)
                if checkField.harvested == False:
                    return Response({"error": "Field not harvested, harvest it to plant new crop"}, status=400)
                else:
                    checkField.harvested = False
                    checkField.save()
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save plantation info"}, status=400)

# get plantation info
class GetPlantation(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            plantation = Plantation.objects.filter(field=id).order_by('-id')
            serializer = PlantationSerializer(plantation, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get plantation info"}, status=400)

#add fertilizer addition
class AddFertilizer(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = FertilizerAdditionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save fertilizer addition"}, status=400)

# get fertilizer addition
class GetFertilizer(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            fertilizer = FertilizerAddition.objects.filter(field=id).order_by('-id')
            serializer = FertilizerAdditionSerializer(fertilizer, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get fertilizer addition"}, status=400)


# add pest control
class AddPestControl(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = PestControlSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save pest control"}, status=400)


# get pest control
class GetPestControl(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            pestControl = PestControl.objects.filter(field=id).order_by('-id')
            serializer = PestControlSerializer(pestControl, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get pest control"}, status=400)    


# add irrigation
class AddIrrigation(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = IrrigationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save irrigation"}, status=400)
    

# get irrigation
class GetIrrigation(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            irrigation = Irrigation.objects.filter(field=id).order_by('-id')
            serializer = IrrigationSerializer(irrigation, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get irrigation"}, status=400)
    

# add harvest
class AddHarvest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = HarvestSerializer(data=request.data)
            if serializer.is_valid():
                fieldId = request.data.get("field")
                cropToHarvest = request.data.get("crop")
                checkPlantation = Plantation.objects.filter(Q(field=fieldId) & Q(crop=cropToHarvest)).order_by('-id')
                if not checkPlantation:
                    return Response({"error": "Field already harvested, new crop not planted"}, status=400)
                checkField = Fields.objects.get(id=fieldId)
                if checkField.harvested == True:
                    return Response({"error": "Field already harvested, new crop not planted"}, status=400)
                checkField.harvested = True
                checkField.save()
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save harvest"}, status=400)
    

# get harvest
class GetHarvest(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            harvest = Harvest.objects.filter(field=id).order_by('-id')
            serializer = HarvestSerializer(harvest, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get harvest"}, status=400)


#get all field activities
class GetAllFieldActivities(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            plantation = Plantation.objects.filter(field=id).order_by('-id')
            fertilizer = FertilizerAddition.objects.filter(field=id).order_by('-id')
            pestControl = PestControl.objects.filter(field=id).order_by('-id')
            irrigation = Irrigation.objects.filter(field=id).order_by('-id')
            harvest = Harvest.objects.filter(field=id).order_by('-id')
            plantationSerializer = PlantationSerializer(plantation, many=True)
            fertilizerSerializer = FertilizerAdditionSerializer(fertilizer, many=True)
            pestControlSerializer = PestControlSerializer(pestControl, many=True)
            irrigationSerializer = IrrigationSerializer(irrigation, many=True)
            harvestSerializer = HarvestSerializer(harvest, many=True)
            return Response({
                "plantation": plantationSerializer.data,
                "fertilizer": fertilizerSerializer.data,
                "pestcontrol": pestControlSerializer.data,
                "irrigation": irrigationSerializer.data,
                "harvestcrop": harvestSerializer.data
            }, status=200)
        except:
            return Response({"error": "Failed to get field activities"}, status=400)    



# scrape and get data
class ScrapeData(APIView):
    permission_classes = []
    
    def get(self, request, location):
        try:
            if location == "all":
                return Response({"data": scrape.getAll()}, status=200)
            else:
                return Response({"data": scrape.getFrom(location)}, status=200)
        except:
            return Response({"error": "Failed to scrape data"}, status=400)


# set pinned location
class SetPinnedLocation(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = PinnedLocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({"error": "Failed to save pinned location"}, status=400)

# get pinned location
class GetPinnedLocation(APIView):
    permission_classes = []
    
    def get(self, request):
        try:
            pinned = PinnedLocation.objects.all().order_by('-id')[0]
            serializer = PinnedLocationSerializer(pinned, many=False)
            return Response(serializer.data, status=200)
        except:
            return Response({"error": "Failed to get pinned location"}, status=400)


# delete all qna
class DeleteAllFrequentQuestions(APIView):
    permission_classes = []
    
    def delete(self, request):
        try:
            FrequentQuestions.objects.all().delete()
            return Response({"message": "All questions deleted"}, status=204)
        except:
            return Response({"error": "Failed to delete questions"}, status=400)
        
# delete all fields
