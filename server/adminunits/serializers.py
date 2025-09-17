from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adminunits.models import Unit


class UnitUpdateSerializer(serializers.ModelSerializer):
    message = 'Поля lat или lon должны быть оба заполнены или пусты'

    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)
    class Meta:
        model = Unit
        fields = ['point', 'type', 'start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day', 'lat', 'lon']
        extra_kwargs = {
            'point': {'required': False},
            'type': {'required': False},
            'start_year': {'required': False},
            'start_month': {'required': False},
            'start_day': {'required': False},
            'end_year': {'required': False},
            'end_month': {'required': False},
            'end_day': {'required': False},
        }

    def validate(self, data):
        point = self.instance.point
        if point:
            current_lat, current_lon = list(point)
            if 'lat' in data and 'lon' in data:
                lat, lon = data['lat'], data['lon']
                if lat is None and lon is None:
                    data['point'] = None
                elif lat and lon:
                    data['point'] = Point(lat, lon)
                else:
                    raise ValidationError(self.message)
            elif 'lat' in data and data['lat']:
                data['point'] = Point(data['lat'], current_lon)
            elif 'lon' in data and data['lon']:
                data['point'] = Point(current_lat, data['lon'])
            else:
                raise ValidationError(self.message)
        else:
            lat, lon = data.get('lat'), data.get('lon')
            if lat and lon:
                data['point'] = Point(float(lat), float(lon))
            else:
                raise ValidationError(self.message)

        data.pop('lat', None)
        data.pop('lon', None)        
        return data
