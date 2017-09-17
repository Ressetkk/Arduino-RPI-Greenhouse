from django import forms

class UpdateFieldsForm(forms.Form):
    temp_val = forms.CharField(label='Ustalona temperatura C', max_length=2, widget = forms.TextInput(attrs={'class':'form-control'}))
    hum_val = forms.CharField(label='Ustalona wilgotnosc %', max_length=3, widget = forms.TextInput(attrs={'class':'form-control'}))
    temp_range = forms.CharField(label='Zakres temperatury C', max_length=2, widget = forms.TextInput(attrs={'class':'form-control'}))
    _choices = [('True', 'Wlaczony'),('False','Wylaczony')]
    led_power = forms.ChoiceField(choices=_choices, widget=forms.RadioSelect())
