from rest_framework import serializers

class CustomDateField(serializers.DateField):
    def __init__(self, **kwargs):
        kwargs["input_formats"] = ["%d/%m/%Y"]
        kwargs["format"] = "%d/%m/%Y"
        super().__init__(**kwargs)
