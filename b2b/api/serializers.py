from rest_framework import serializers
from .models import Company, Order, Product, OrderPosition

class CompanySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj.type==0:
            return 'seller'
        else:
            return 'buyer'

    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderPositionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderPosition
        fields = ('id', 'product', 'quantity', 'elem_price', 'sum_price')
        read_only_fields = ('product', 'id', 'elem_price', 'sum_price')

class OrderSerializer(serializers.ModelSerializer):
    company_seller = CompanySerializer(read_only=True)
    company_buyer = CompanySerializer(read_only=True)
    positions = serializers.SerializerMethodField()

    def get_positions(self, obj):
        queryset = OrderPosition.objects.filter(order=obj)
        return OrderPositionSerializer(queryset, many=True).data

    class Meta:
        model = Order
        fields = '__all__'
