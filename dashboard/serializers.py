from rest_framework.serializers import ModelSerializer
from .models import TickerName, Trades, UserTrades
from rest_framework import serializers


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class TickerNameSerializer(ModelSerializer):
    class Meta:
        model = TickerName
        fields = '__all__'


class CreateTradeFormSerializer(ModelSerializer):
    ticker_name = serializers.CharField(validators=[required])
    entry_price = serializers.IntegerField(validators=[required])
    target_price = serializers.IntegerField(validators=[required])
    stop_loss = serializers.IntegerField(validators=[required])
    # ticker_type = serializers.RelatedField(validators=[required()])

    class Meta:
        model = Trades
        fields = '__all__'


class SlTpDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trades
        fields = '__all__'


class TradeListAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Trades
        fields = '__all__'


class UserTradeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrades
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return validated_data