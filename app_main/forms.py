from django import forms

from app_main.models import Config, Product, Property


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
