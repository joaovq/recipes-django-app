from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import Recipes
from app.permissions import IsOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from app.serializers import RecipeSerializer, TagSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from tag.models import Tag
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeApiv2ViewSet(ModelViewSet):
    queryset = Recipes.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
                qs = qs.filter(category_id=category_id)

        return qs

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):  # POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        serializer = RecipeSerializer(
            instance=self.get_object(),
            data=request.data,
            context={'request': request},
            many=False,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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


class RecipeApiV2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipes.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = RecipeSerializer(
            instance=self.get_queryset().filter(pk=pk).first(),
            data=request.data,
            context={'request': request},
            many=False,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    # def get_recipe(self,pk):
    #     return get_object_or_404(
    #         Recipes.objects.get_published(),
    #         pk=pk
    #     )
    # def get(self, request,pk):
    #     serializer = RecipeSerializer(
    #         instance=self.get_recipe(pk), context={'request': request}, many=False
    #     )
    #     return Response(serializer.data)
    # def patch(self,request, pk):
    #     serializer = RecipeSerializer(
    #         instance=self.get_recipe(pk),
    #         data=request.data,
    #         context={'request': request},
    #         many=False,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    # def delete(self, request, pk):
    #     self.get_recipe(pk).delete()
    #     return Response(status = status.HTTP_204_NO_CONTENT)

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
        return Response(status=status.HTTP_204_NO_CONTENT)
