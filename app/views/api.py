from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import Recipes
from app.serializers import RecipeSerializer, TagSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from tag.models import Tag
from rest_framework.pagination import PageNumberPagination

class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 10

class RecipeApiV2List(ListCreateAPIView):
    queryset = Recipes.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    # def get(self, request):
    #     recipes = Recipes.objects.get_published()[:10]
    #     serializer = RecipeSerializer(
    #         instance=recipes, many=True, context={'request': request})
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = RecipeSerializer(
    #         data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(author_id=1, category_id=2, tags=[1, 2])
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )

class RecipeApiV2Detail(APIView):
    def get_recipe(self,pk):
        return get_object_or_404(
            Recipes.objects.get_published(),
            pk=pk
        )
    def get(self, request,pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk), context={'request': request}, many=False
        )
        return Response(serializer.data)
    def patch(self,request, pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk),
            data=request.data,
            context={'request': request},
            many=False,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        self.get_recipe(pk).delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# @api_view(http_method_names=['get', 'post'])
# def recipe_list(request):
#     if request.method == 'GET':
        
#     elif request.method == 'POST':
        
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(http_method_names=['get'])
# def recipe_api_details(request, pk):
    
#     if request.method == 'GET':
        
#     elif request.method == 'PATCH':
        
#     elif request.method == 'DELETE':
        


@api_view(http_method_names=['get', 'patch', 'delete'])
def tag_api_details(request, pk):
    tag = get_object_or_404(
            Tag.objects.all(),
            pk=pk
        )
    if request.method == 'GET':
        serializer = TagSerializer(instance=tag, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TagSerializer(data=tag, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'DELETE':
        return Response(status = status.HTTP_204_NO_CONTENT)
