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

        """override create to create new tems"""

        items_data = validated_data.pop('items', None)
        bill = bill_model.Bill.objects.create(**validated_data)

        if items_data:
            for item_data in items_data:
                item = bill_model.Item.objects.create(sale=bill, **item_data)

        return bill

    def update(self, instance, validated_data):

        """new entries are created , existing entries are updated
           entry which are not present in validated are removed from database"""

        validated_items = validated_data.pop("items")

        bill = super().update(instance, validated_data)

        items = bill.items.all()
        existing_item_ids = [item.id for item in items ]

        if items:
            for item_data in items:
                if item_data.id in existing_item_ids:
                    instance = bill_model.Item.objects.get(id=item_data.id)
                    instance.item = validated_items['item']
                    instance.amount = validated_items['amount']
                    instance.save()
                    existing_item_ids.remove(item_data.id)
                else:
                    bill_model.Item.objects.craete(sale=bill, **item_data)

        for data in existing_item_ids:
            item = bill_model.Item.objects.get(id=data.id)
            item.delete()

        return bill


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Service
        fields = "__all__"


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Entries
        fields = "__all__"