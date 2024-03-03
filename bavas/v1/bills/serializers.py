from rest_framework import serializers
from v1.bills import models as bill_model
#
#


class ItemSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    class Meta:
        model = bill_model.Item
        fields = ['id', 'item', 'amount']


class BillSerializer(serializers.ModelSerializer):


    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = bill_model.Bill
        fields = "__all__"


    def create(self, validated_data):

        items_data = validated_data.pop('items', None)
        bill = bill_model.Bill.objects.create(**validated_data)

        if items_data:
            for item_data in items_data:
                item = bill_model.Item.objects.create(sale=bill, **item_data)

        return bill

    def update(self, instance, validated_data):

        items = validated_data.pop("items")

        order = super().update(instance, validated_data)

        return instance


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Service
        fields = "__all__"


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Entries
        fields = "__all__"