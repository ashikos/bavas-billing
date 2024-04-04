from rest_framework import serializers
from v1.bills import models as bill_model
from common import library as comm_libs


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
                item = bill_model.Item.objects.create(bill=bill, **item_data)
        return bill

    def update(self, instance, validated_data):

        """new entries are created , existing entries are updated
           entry which are not present in validated are removed from database"""

        if "items" in validated_data.keys():
            validated_items = validated_data.pop("items")

        bill = super().update(instance, validated_data)

        items = bill.items.all()
        existing_item_ids = [item.id for item in items]

        if items:
            for item_data in validated_items:
                item_data = dict(item_data)
                if "id" in item_data.keys() and item_data["id"] in existing_item_ids:
                    instance = bill_model.Item.objects.get(id=item_data["id"])
                    instance.item = item_data['item']
                    instance.amount = item_data['amount']
                    instance.save()
                    existing_item_ids.remove(item_data["id"])
                else:
                    bill_model.Item.objects.create(bill=bill, **item_data)

        for id in existing_item_ids:
            item = bill_model.Item.objects.get(id=id)
            item.delete()

        return bill


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Service
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Customer
        fields = "__all__"


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_model.Entries
        fields = "__all__"

    def create(self, validated_data):
        # date = validated_data.pop("date")
        # date = comm_libs.convert_str_to_datetime(date, '%d/%m/%Y')
        # validated_data["date"] = date
        # print(date, type(date))
        entry = super().create(validated_data)
        return entry
