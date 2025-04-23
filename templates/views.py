from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CertificateTemplate
from .serializers import CertificateTemplateSerializer

class CertificateTemplateViewSet(viewsets.ModelViewSet):
    queryset = CertificateTemplate.objects.all()
    serializer_class = CertificateTemplateSerializer
    parser_classes = (MultiPartParser, FormParser)  # ✅ Allow file uploads

    @action(detail=False, methods=["post"], url_path="upload")
    def upload_template(self, request, *args, **kwargs):
        """ ✅ Custom Upload Endpoint: `/api/templates/upload/` """
        serializer = self.get_serializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Template uploaded successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
