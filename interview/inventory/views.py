from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType
from interview.inventory.schemas import InventoryMetaData
from interview.inventory.serializers import InventoryLanguageSerializer, InventorySerializer, InventoryTagSerializer, InventoryTypeSerializer

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from datetime import datetime

class InventoryListGetItemsView(APIView):
    serializer_class = InventorySerializer
    max_limit = 3 # Maximum items per page

    def get(self, request: Request, *args, **kwargs) -> Response:
        created_after_str = request.query_params.get('created_after', None)
        page_num = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', self.max_limit)

        if not created_after_str:
            return Response({'error': 'created_after parameter is required'}, status=400)

        try:
            created_after = datetime.fromisoformat(created_after_str.replace('Z', '+00:00'))
        except ValueError:
            return Response({'error': 'Invalid created_after date format. Please use ISO format.'}, status=400)

        try:
            limit = int(limit)
        except ValueError:
            return Response({'error': 'Limit must be an integer'}, status=400)

        limit = min(limit, self.max_limit) # Ensure limit does not exceed max_limit

        queryset = Inventory.objects.filter(created_at__gt=created_after).order_by('created_at')
        paginator = Paginator(queryset, limit)

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            return Response({'data': [], 'message': 'Page is empty'}, status=200)

        serializer = self.serializer_class(page.object_list, many=True)
        return Response(serializer.data, status=200)

class InventoryListCreateView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            metadata = InventoryMetaData(**request.data['metadata'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
        request.data['metadata'] = metadata.dict()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()
    

class InventoryRetrieveUpdateDestroyView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTagListCreateView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryTagRetrieveUpdateDestroyView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory_tag)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory_tag, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs['id'])
        inventory_tag.delete()
        
        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryLanguageListCreateView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryLanguageRetrieveUpdateDestroyView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
    

class InventoryTypeListCreateView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=201)
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)
        
        return Response(serializer.data, status=200)
    
    def get_queryset(self):
        return self.queryset.all()


class InventoryTypeRetrieveUpdateDestroyView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    
    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory)
        
        return Response(serializer.data, status=200)
    
    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        
        return Response(serializer.data, status=200)
    
    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs['id'])
        inventory.delete()
        
        return Response(status=204)
    
    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)