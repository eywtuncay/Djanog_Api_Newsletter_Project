from rest_framework import serializers
from haberler.models import Makale, Gazeteci

from datetime import datetime
from datetime import date
from django.utils.timesince import timesince



class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()

    class Meta:
        model = Makale
        fields = '__all__'
        read_only_fields = ['id', 'yaratilma_tarihi', 'güncellenme_tarihi']

    def get_time_since_pub(self, obj):
        now = datetime.now()
        pub_date = obj.yayimlanma_tarihi
        if obj.aktif:
            time_delta = timesince(pub_date, now)
            return time_delta
        return 'Aktif Değil'

    def validate_yayimlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yayımlanma tarihi ileri bir tarih olamaz.')
        return tarihdegeri

    # Alan seviyesinde validasyon
    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Başlık alanı minimum 20 karakter olmalı. Girilen: {len(value)} karakter.')
        return value

    # Obje seviyesinde validasyon
    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Başlık ve Açıklama alanları farklı olmalı.')
        return data



class GazeteciSerializers(serializers.ModelSerializer):

    # makaleler = MakaleSerializer(many=True, read_only=True)

    makaleler = serializers.HyperlinkedRelatedField(
        many = True,
        read_only=True,
        view_name = 'makale-detay',
    )

    class Meta:
        model = Gazeteci
        fields = '__all__'





# ----------- STANDART ÖRNEK SERIALIZER -----------

class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayimlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncellenme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance


    def validate(self, data):   #object level
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Başlık ve Açıklama alanları farklı olmalı.')
        return data

    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Başlık alanı minumum 20 karakter olmalı. Girilen: {len(value)} karakter.')
        return value


