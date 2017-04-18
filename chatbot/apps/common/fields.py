from django.forms import ModelChoiceField


class NameModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name if hasattr(obj, 'name') else str(obj)
