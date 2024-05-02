from django import forms

Opcion1 = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
Opcion2 = [
    ('$25,000', '$25,000'),
    ('$50,000', '$50,000'),
    ('$100,000', '$100,000'),
    ('$150,000', '$150,000'),
    ('$250,000', '$250,000'),
    ('$500,000', '$500,000'),
]
Opcion3 = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
]
Opcion4 = [
    ('Si', 'Si'),
    ('No', 'No'),
]
Opciones5 = [
    ('Mensual', 'Mensual'),
    ('Trimestral', 'Trimestral'),
    ('Semestral', 'Semestral'),
    ('Anual', 'Anual'),
]
class C_Intermediario2(forms.Form):
    Nombre = forms.CharField(label="Nombre de Empresa:", max_length=200, required=False)
    Int = forms.CharField(label="Intermediario:", max_length=200, required=False)
    Tel = forms.CharField(label="Teléfono:", max_length=200, required=False)
    Correo = forms.CharField(label="Correo electrónico:", max_length=200, required=False)
    Id = forms.CharField(label="IVD o CVD:", max_length=200, required=False) 
    
class form_CotizadorTAR(forms.Form):
    Sol = forms.CharField(label="Solicitante:", max_length=200)
    Nac = forms.CharField(label="Fecha de Nacimiento (YYYY/MM/DD):", max_length=200)
    Gen = forms.ChoiceField(label="Género:", choices=Opcion1, widget=forms.Select(attrs={'id':'gen'}))
    Sum = forms.ChoiceField(label="Suma Asegurada:", choices=Opcion2 , widget=forms.Select(attrs={'id':'sum'}))
    Riesgo = forms.ChoiceField(label="Seleccione la clasificación según corresponda:", choices=Opcion3, widget=forms.Select(attrs={'id':'riesgo'}))
    TipoA = forms.CharField(label="Riesgo A",initial="Ocupaciones normalmente realizadas en oficinas, cómo: Abogados, Maestros, Médicos, Personal de Oficina, comercios, operadores de equipo de procesamiento de datos y operaciones manuales sedentarias de tipo liviano como: Dentistas, dermatólogos, cirujanos, dibujantes, fotógrafos, personal de venta de tiendas y almacenes." ,widget=forms.Textarea(attrs={'readonly':'readonly', 'class': 'tipa'}))
    TipoB = forms.CharField(label="Riesgo B",initial="Ocupaciones normalmente realizadas fuera de los locales de oficina, cómo: Arquitectos, Agentes o Asesores de Venta, Personal paramédico, personal de empresas de construcción, en general personal que realiza actividades de riesgo medio." ,widget=forms.Textarea(attrs={'readonly':'readonly', 'class': 'tipb'}))
    TipoC = forms.CharField(label="Riesgo C",initial="Ocupaciones realizadas utilizando normalmente herramienta y maquinaria, cómo: Personal operador manual de máquinas en fábricas, talleres, Personal que labora en construcción, montaje, demolición e instalación, Personal que labora en actividades agrícolas y pecuarias, Personal militar o de seguridad, Conductores de vehículos pesados y/o de transporte público." ,widget=forms.Textarea(attrs={'readonly':'readonly', 'class': 'tipc'}))
    Titulo = forms.CharField(label="", initial="Coberturas Adicionales:", widget=forms.Textarea(attrs={'readonly':'readonly', 'class': 'Adicional'}))
    Ben = forms.ChoiceField(label="(ITP y Pérdida de miembros, Renta Diaria por Incapacidad Temporal, Reembolso de Gastos Médicos y Gastos Funerarios)", choices=Opcion4, widget=forms.Select(attrs={'id':'ben'}))
    Temp = forms.ChoiceField(label="Forma de Pago", choices=Opciones5, widget=forms.Select(attrs={'id':'temp'}))
    Mail = forms.CharField(label="Correo Electrónico", max_length=200, required=False)
    Cellphone = forms.CharField(label="Celular:", max_length=200)
