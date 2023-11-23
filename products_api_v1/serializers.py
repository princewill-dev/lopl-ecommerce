from rest_framework import serializers
from .models import Pack, Product


from rest_framework import serializers
from .models import Pack, Product

class ProductSerializer(serializers.ModelSerializer):
    product_variants = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_category', 'product_type', 'product_variants', 'product_image']

class PackSerializer(serializers.ModelSerializer):
    pack_products = ProductSerializer(many=True)

    class Meta:
        model = Pack
        fields = ['pack_name', 'pack_price', 'pack_image', 'pack_type', 'pack_product_number', 'pack_products']

    def create(self, validated_data):
        products_data = validated_data.pop('pack_products')
        pack = Pack.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(pack=pack, **product_data)
        return pack


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

# class PackSerializer(serializers.ModelSerializer):
#     pack_products = ProductSerializer(many=True, read_only=True)
    
#     class Meta: 
#         model = Pack
#         fields = '__all__'


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'product_price', 'product_category', 'product_type', 'product_image', 'products_variants']



# class ProductVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariant
#         fields = ('product_variant_name',)

# class ProductSerializer(serializers.ModelSerializer):
#     products_variants = ProductVariantSerializer(many=True, read_only=True)

#     class Meta:
#         model = Product
#         fields = ('product_name', 'product_price', 'product_category', 'product_type', 'product_id', 'product_image', 'products_variants')

# class PackSerializer(serializers.ModelSerializer):
#     pack_products = ProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = Pack
#         fields = ('pack_products', 'pack_price', 'pack_id', 'pack_name', 'pack_image', 'pack_type', 'pack_product_number')