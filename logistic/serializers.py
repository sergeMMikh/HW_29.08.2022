from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['address', "positions"]

    def create(self, validated_data):
        print(f'validated_data: {validated_data}')
        # достаем связанные данные для других таблиц

        positions = validated_data.pop('positions')
        print(f'positions: {positions}')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position in positions:
            try:
                obj = StockProduct.objects.get(stock=stock, price=position.get('price'))
                setattr(obj, 'quantity', position.get('quantity'))
                setattr(obj, 'price', position.get('price'))
                obj.save()
            except StockProduct.DoesNotExist:
                StockProduct.objects.create(stock=stock, **position)

            # StockProduct.objects.update_or_create(stock=stock, **position,
            #                                       defaults={'quantity': position.get('quantity'),
            #                                                 'price' :position.get('price')})

        return stock
