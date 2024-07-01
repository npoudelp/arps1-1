from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .gemini import ask_gemini
from .models import Fields, FrequentQuestions
from .serializers import FieldsSerializer, FrequentQuestionsSerializer
from .recomend import recomendCrop


class AddField(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FieldsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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
            field = Fields.objects.get(id=id)
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
            field.delete()
            return Response({"message": "Field deleted"}, status=204)
        except Fields.DoesNotExist:
            return Response({"error": "Field not found"}, status=404)



#  get gemini response
class GetGeminiResponse(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question = request.data.get("question")
        if question is None:
            return Response({"error": "Question not provided"}, status=400)
        try:
            response = ask_gemini(question)
            return Response({
                "response": response,
                "question": question
            }, status=200)
        except:
            return Response({"error": "Question not recognised"}, status=400)
        

# add frequent questions
class AddFrequentQuestion(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FrequentQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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