from rest_framework import serializers
from shop.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class GetChildCategory():
    def get_child_category(self, obj):
        serializer = CategorySerializerTree(
            instance=obj.children.all(),
            many=True
        )
        return serializer.data


class CategorySerializerTree(serializers.ModelSerializer, GetChildCategory):
    products = ProductSerializer(many=True)
    children = serializers.SerializerMethodField(
        method_name="get_child_category",
    )

    # def get_queryset(self):
    #    return Category.objects.filter(parent=None)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'children']
        extra_kwargs = {'id': {'read_only': True},
                        'products': {'read_only': True},
                        'children': {'read_only': True},
                        }


class CategorySerializerTreeAdd(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent_category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'parent_category',
                  ]
        kwargs = {'id': {'read_only': True},
                  }


class BucketPostSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
