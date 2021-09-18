from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins , status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag , Ingredient , Recipe

from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the databse"""
    queryset = Tag.objects.all()
    serializers_class = serializers.TagSerializer

    
class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the databse"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """"Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _paras_to_ints(self, qs):
        """Converst a list of strings IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]


    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tag = self.request.query_params.get('tag')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeSerializer
        elif self.action== 'upload_image':
            return serializers.RecipeImageSerializer


        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'] , detail = True , url_path='upload-image')
    def upload_image(self, request , pk=None):
        """Upload and image to a recipe""" 
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# class TagViewSet(viewsets.GenericViewSet , mixins.ListModelMixin , 
#                                            mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer

#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
        
#     def perform_create(self, serializer):
#         """"Create a new tag"""
#         serializer.save(user=self.request.user)
        

# class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin ,
#                                                  mixins.CreateModelMixin):
#     """Manage ingredient in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer

#     def get_queryset(self):
#         """"Return objects for the current authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
    
#     def perform_create(self, serializer):
#         """"Create a new ingrediente"""
#         serializer.save(user=self.request.user)