from django.shortcuts import render
from django.db.models import Count, OuterRef, Subquery
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.generics import DestroyAPIView

from .models import Company, Order, Product, OrderPosition
from .serializers import CompanySerializer, ProductSerializer, OrderPositionSerializer, OrderSerializer

# Create your views here.


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        product = serializer.save(company = Company.objects.get(pk=self.request.data['company']['id']))

    def perform_update(self, serializer):
        if 'company' in self.request.data:
            serializer.save(company = Company.objects.get(pk=self.request.data['company']['id']))
        else:
            serializer.save()


class OrderViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        company_seller = Company.objects.get(pk=self.request.data['seller']['id'])
        company_buyer = Company.objects.get(pk=self.request.data['buyer']['id'])
        order = Order.objects.create(company_seller=company_seller, company_buyer=company_buyer)
        order.save()

        positions = request.data['positions']
        for position in positions:
            product = Product.objects.get(pk=position['product']['id'])
            quantity = position['quantity']
            elem_price = product.price
            sum_price = product.price * position['quantity']
            new_position = OrderPosition.objects.create(product=product,
                                                        order=order,
                                                        quantity=quantity,
                                                        elem_price=elem_price,
                                                        sum_price=sum_price)
            new_position.save()

        return Response(OrderSerializer(order).data)


class RemoveNoOrderBuyersView(DestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def delete(self, request, *args, **kwargs):
        company_orders = Order.objects.filter(company_buyer=OuterRef('pk'))
        queryset = Company.objects.annotate(count=Count(Subquery(company_orders.values('id')[:1]))).filter(type=1, count=0)
        print('!!!!!', len(queryset))

        for elem in queryset:
            elem.is_active = False
            elem.save()

        return Response(status=status.HTTP_204_NO_CONTENT)