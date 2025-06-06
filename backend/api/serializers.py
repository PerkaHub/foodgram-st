import base64
import binascii

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from const.errors import ERROR_MESSAGES
from const.const import (
    MIN_COOKING_TIME,
    MIN_INGREDIENT_AMOUNT,
    ALLOWED_IMAGE_FORMATS,
)
from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
)


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Поле для кодирования/декодирования изображения Base64"""

    def to_internal_value(self, data):
        try:
            if isinstance(data, str) and data.startswith("data:image"):
                parts = data.split(";base64,")
                if len(parts) != 2:
                    raise serializers.ValidationError(
                        ERROR_MESSAGES["invalid_base64"]
                    )

                format_part = parts[0]
                imgstr = parts[1]

                ext = format_part.split("/")[-1]
                if ext not in ALLOWED_IMAGE_FORMATS:
                    raise serializers.ValidationError(
                        ERROR_MESSAGES["invalid_image_format"]
                    )

                try:
                    decoded_file = base64.b64decode(imgstr)
                except (TypeError, binascii.Error):
                    raise serializers.ValidationError(
                        ERROR_MESSAGES["invalid_base64_data"]
                    )

                data = ContentFile(decoded_file, name=f"photo.{ext}")

            return super().to_internal_value(data)

        except Exception as e:
            raise serializers.ValidationError(str(e))


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "is_subscribed",
            "avatar",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.follower.filter(author=obj).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Укороченный сериализатор для рецептов в подписках"""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source="recipes.count", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "is_subscribed",
            "avatar",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes = obj.recipes.all()

        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit and recipes_limit.isdigit():
            recipes = recipes[: int(recipes_limit)]

        return ShortRecipeSerializer(
            recipes,
            many=True,
            context=self.context).data


class RecipeIngredientCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(min_value=MIN_INGREDIENT_AMOUNT)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_items', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "author",
            "text",
            "image",
            "ingredients",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.shopping_carts.filter(recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(allow_null=True)
    ingredients = RecipeIngredientCreateSerializer(many=True, write_only=True)
    cooking_time = serializers.IntegerField(min_value=MIN_COOKING_TIME)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "image",
            "ingredients",
            "cooking_time",
        )

    def validate(self, data):
        request = self.context.get('request')
        method = request.method if request else None

        if method in ["POST", "PATCH", "PUT"]:
            if 'ingredients' not in data:
                raise serializers.ValidationError(
                    {"ingredients": [ERROR_MESSAGES["no_ingredients"]]}
                )
            ingredients = data['ingredients']
            if not ingredients:
                raise serializers.ValidationError(
                    {"ingredients": [ERROR_MESSAGES["empty_ingredients"]]}
                )
            ingredient_ids = set()
            for ingredient in ingredients:
                if not isinstance(ingredient, dict) or 'id' not in ingredient:
                    raise serializers.ValidationError(
                        {"ingredients": [ERROR_MESSAGES["invalid_format"]]}
                    )
                if ingredient['id'] in ingredient_ids:
                    raise serializers.ValidationError(
                        {"ingredients": [ERROR_MESSAGES["repeat_ingredients"]]}
                    )
                ingredient_ids.add(ingredient['id'])
        return data

    def _create_ingredients(self, recipe, ingredients_data):
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data["id"],
                amount=ingredient_data["amount"],
            )
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def _update_ingredients(self, recipe, ingredients_data):
        recipe.ingredients_items.all().delete()
        self._create_ingredients(recipe, ingredients_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        validated_data['author'] = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        self._create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        instance = super().update(instance, validated_data)

        if "image" in validated_data:
            instance.image = validated_data.get("image", instance.image)
            instance.save()

        if ingredients_data is not None:
            self._update_ingredients(instance, ingredients_data)

        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


class AddAvatar(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ("avatar",)
