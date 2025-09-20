from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adminunits.models import Unit, UnitName, Including


class UnitUpdateSerializer(serializers.ModelSerializer):
    message = 'Поля lat или lon должны быть оба заполнены или пусты'

    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)
    class Meta:
        model = Unit
        fields = ['point', 'type', 'start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day', 'lat', 'lon']
        # extra_kwargs = {
        #     'point': {'required': False},
        #     'type': {'required': False},
        #     'start_year': {'required': False},
        #     'start_month': {'required': False},
        #     'start_day': {'required': False},
        #     'end_year': {'required': False},
        #     'end_month': {'required': False},
        #     'end_day': {'required': False},
        # }

    def validate(self, data):
        if 'lat' in data or 'lon' in data:
            point = self.instance.point
            if point:
                current_lon, current_lat = list(point)
                if 'lat' in data and 'lon' in data:
                    lat, lon = data['lat'], data['lon']
                    if lat is None and lon is None:
                        data['point'] = None
                    elif lat and lon:
                        data['point'] = Point(lon, lat)
                    else:
                        raise ValidationError(self.message)
                elif 'lat' in data and data['lat']:
                    data['point'] = Point(current_lon, data['lat'])
                elif 'lon' in data and data['lon']:
                    data['point'] = Point(data['lon'], current_lat)
                else:
                    raise ValidationError(self.message)
            else:
                lat, lon = data.get('lat'), data.get('lon')
                if lat and lon:
                    data['point'] = Point(float(lon), float(lat))
                elif lat or lon:
                    raise ValidationError(self.message)

            data.pop('lat', None)
            data.pop('lon', None)
 
        return data


# class DateSerialzer(serializers.Serializer):
#     year = serializers.IntegerField(allow_null=True)
#     month = serializers.IntegerField(allow_null=True)
#     day = serializers.IntegerField(allow_null=True)


class UnitUpdateParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Including
        fields = [
            'parent', 'start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day',
        ]


class UnitUpdateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitName
        fields = [
            'name', 'start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day',
        ]


class UnitCreateSerializer(serializers.ModelSerializer):
    message = 'Поля lat или lon должны быть оба заполнены или пусты'

    lat = serializers.FloatField(allow_null=True)
    lon = serializers.FloatField(allow_null=True)
    parent_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField()
    class Meta:
        model = Unit
        fields = [
            'point', 'type', 'start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day',
            'lat', 'lon', 'parent_id', 'name',
        ]

    def create(self, validated_data):
        parent_id = validated_data.pop('parent_id')
        name = validated_data.pop('name')
        with transaction.atomic():
            unit = Unit.objects.create(**validated_data)
            UnitName.objects.create(unit=unit, name=name)
            if parent_id:
                Including.objects.create(child=unit, parent_id=parent_id)

        return unit

    def validate(self, data):
        lat, lon = data.get('lat'), data.get('lon')
        if lat and lon:
            data['point'] = Point(float(lon), float(lat))
        elif lat or lon:
            raise ValidationError(self.message)

        data.pop('lat', None)
        data.pop('lon', None) 
        return data
