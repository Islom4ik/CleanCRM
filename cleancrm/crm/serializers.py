from rest_framework import serializers

from .models import Leads, Lead_comments

class LeadFilterSerializer(serializers.Serializer):
    date = serializers.CharField(required=True, max_length=10)
    operator = serializers.CharField(required=True)
    product = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    def create(self, validated_data):
        return Leads.objects.create(**validated_data)

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'

class LeadAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = ('name', 'phone', 'request_date', 'address', 'product')

class LeadEditSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=True)
    lead_phone = serializers.CharField(required=True)
    lead_status = serializers.CharField(required=True)
    lead_product = serializers.CharField(required=True)
    lead_address = serializers.CharField(required=True)
    lead_soldcount = serializers.CharField(required=True, allow_null=True)
    lead_soldprice = serializers.IntegerField(required=True, allow_null=True)
    lead_callcount = serializers.IntegerField(required=True, allow_null=True)
    lead_calldate = serializers.CharField(required=True, allow_null=True)
    solddate = serializers.CharField(required=True, allow_null=True)


class OperatorAddLeadsSerializer(serializers.Serializer):
    leads = serializers.ListField(required=True, child=serializers.IntegerField())
    operator = serializers.IntegerField(required=True)

class CommentsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead_comments
        fields = '__all__'