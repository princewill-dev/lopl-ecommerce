from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import PackSerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class CreatePackView(APIView):

    @swagger_auto_schema(
        operation_description="This endpoint creates a new product.",
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Product created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'product': openapi.Schema(type=openapi.TYPE_OBJECT, 
                            properties={
                                'product_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'product_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'product_price': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'product_category': openapi.Schema(type=openapi.TYPE_STRING),
                                'product_type': openapi.Schema(type=openapi.TYPE_STRING),
                                'product_variants': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'product_image': openapi.Schema(type=openapi.TYPE_STRING, description='Base64 encoded string of the product image')
                            })
                    },
                ),
            ),
        }
    )

    def post(self, request):
        serializer = PackSerializer(data=request.data)  
        if serializer.is_valid():
            pack = serializer.save() 
            products = request.data.get('pack_products')
            
            for product in products:
                product['pack'] = pack
                product_serializer = ProductSerializer(data=product)  
                if product_serializer.is_valid():
                    product_serializer.save()  

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# class CreatePackView(APIView):

#     serializer_class = ProductSerializer

    
    

#     def create_pack(request):
#         serializer = PackSerializer(data=request.data) 
#         if serializer.is_valid():
#             pack = serializer.save()
#             products = request.data.get('pack_products')
#             for product in products:
#                 product['pack'] = pack
#                 product_serializer = ProductSerializer(data=product) 
#                 if product_serializer.is_valid(): 
#                     product_serializer.save()  

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, format=None):
    #     serializer = ProductSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Product created successfully', 'product': serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="This endpoint retrieves all products.",
        responses={
            200: openapi.Response(
                description="Products retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT, 
                        properties={
                            'product_id': openapi.Schema(type=openapi.TYPE_STRING),
                            'product_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'product_price': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'product_category': openapi.Schema(type=openapi.TYPE_STRING),
                            'product_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'product_variants': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                        })
                ),
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    



class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    @swagger_auto_schema(
        operation_description="This endpoint retrieves a product by its id.",
        responses={
            200: openapi.Response(
                description="Product retrieved successfully",
                schema=ProductSerializer
            ),
            404: "Product not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class DeleteProductView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    @swagger_auto_schema(
        operation_description="This endpoint deletes a product by its id.",
        responses={
            204: "Product deleted successfully",
            404: "Product not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return response