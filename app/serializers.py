from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.models import Category, Recipes
from author.validators import AuthorRecipeValidator
from tag.models import Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=60)
    # slug = serializers.SlugField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = [
            'id',
            'title',
            'description',
            'author_name',
            'author',
            'category',
            'category_name',
            'tags',
            'public',
            'preparation',
            'tag_objects',
            'tag_links',
            'preparation_time', 'preparation_time_unit',
            'servings_unit',
            'preparation_steps',
            'cover_image'
        ]
    public = serializers.BooleanField(
        source='is_published',
        read_only=True
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True
    )
    # Por default retorna a PK
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(),
    # )
    # Retorna a string da classe do model
    category_name = serializers.StringRelatedField(
        source="category",
        read_only=True
    )
    # author_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all()
    # )
    author_name = serializers.StringRelatedField(source='author',  read_only=True)
    # tags = serializers.PrimaryKeyRelatedField(
    #     queryset=Tag.objects.all(),
    #     many=True
    # )
    tag_objects = TagSerializer(
        many=True, source='tags',
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # View que o click vai redirecionar
        view_name='app:tag_api_detail',
        read_only=True
    )

    # default  def get_preparation(self, recipe):
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('serving_unit') is None:
            attrs['serving_unit'] = self.instance.serving_unit
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
        validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return validate
    
    def validate_title(self, value):
        if len(value)< 5:
            raise serializers.ValidationError('Must have least 5 chars.')
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)