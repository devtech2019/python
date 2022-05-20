from rest_framework import serializers

from .models import s_test


class s_testSerializer(serializers.ModelSerializer):
    class Meta:
        model = s_test
        fields = '__all__'
