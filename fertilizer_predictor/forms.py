from django import forms

class ParametrosForm(forms.Form):
    nome_instancia = forms.CharField(label='Nome da Instância', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 625px;'}))
    temperatura = forms.DecimalField(label='Temperatura', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 625px;'}))
    umidade_ar = forms.DecimalField(label='Umidade do Ar', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 625px;'}))
    umidade_solo = forms.DecimalField(label='Umidade do Solo', widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 625px;'}))
    tipo_solo_choices = (
        ('', 'Abra para selecionar'),
        (0, 'Barrento'),
        (1, 'Arenoso'),
        (2, 'Argiloso'),
        (3, 'Preto'),
        (4, 'Vermelho'),
    )
    tipo_solo = forms.ChoiceField(label='Tipo de Solo', choices=tipo_solo_choices, widget=forms.Select(attrs={'class': 'form-select', 'style': 'width: 624px;'}))
    
    tipo_cultura_choices = (
        ('', 'Abra para selecionar'),
        (0, 'Cana-de-açúcar'),
        (1, 'Algodão'),
        (2, 'Arroz'),
        (3, 'Milho'),
        (4, 'Tabaco'),
        (5, 'Cevada'),
        (6, 'Trigo'),
        (7, 'Painço'),
        (8, 'Sementes para óleo'),
        (9, 'Sementes de leguminosas'),
        (10, 'Nozes'),
    )
    tipo_cultura = forms.ChoiceField(label='Tipo de Cultura', choices=tipo_cultura_choices, widget=forms.Select(attrs={'class': 'form-select', 'style': 'width: 624px;'}))
    
    nitrogenio = forms.DecimalField(label='Nitrogênio', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    fosforo = forms.DecimalField(label='Fósforo', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    potassio = forms.DecimalField(label='Potássio', widget=forms.NumberInput(attrs={'class': 'form-control'}))
