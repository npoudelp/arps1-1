from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Fields
from .serializers import FieldsSerializer


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
        fields = Fields.objects.all()
        serializer = FieldsSerializer(fields, many=True)
        return Response(serializer.data, status=200)