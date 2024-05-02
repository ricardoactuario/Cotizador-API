from django.shortcuts import render
from .forms import C_Intermediario2, form_CotizadorTAR
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import locale
import os
from .models import TR2
from decimal import Decimal
import base64
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import HttpResponse
# Create your views here.

def CotizadorAP(request):
    if request.method == 'GET':
        return render(request, 'S_API.html', {
            'form_intermediario2': C_Intermediario2(),
            'form_CotizadorTAR': form_CotizadorTAR(),
        })
    else:
        buffer = BytesIO()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Crear un objeto PDF
        pdf = canvas.Canvas(buffer)
        #Estilo de Letra
        pdf.setFont("Helvetica", 9)
        #Trabajo con Variables
        Nom = request.POST.get('Nombre', None)
        In = request.POST.get('Int', None)
        Te = request.POST.get('Tel', None)
        Cor = request.POST.get('Correo', None)
        Identificacion = request.POST.get('Id', None)
        Solicitante = request.POST.get('Sol', None)
        Nacimiento = request.POST.get('Nac', None)
        Genero = request.POST.get('Gen', None)
        Tip = request.POST.get('Riesgo', None)
        Bene = request.POST.get('Ben')
        Suma = request.POST.get('Sum', None)

        Mails = request.POST.get('Mail', None)
        Cellphones = request.POST.get('Cellphone', None)

        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        image_path = os.path.join('cotizadorapi', 'static', 'atlanv.png')

        # Agregando contenido al PDF
        pdf.drawString(460, 790, fecha_actual)
            
        pdf.drawImage(image_path, x=50, y=730, width=100, height=40)
            
        pdf.setFont("Helvetica-Bold", 9)
            
        pdf.drawString(240, 740, "OFERTA DE SEGURO DE ACCIDENTES PERSONALES")
            
        pdf.setFont("Helvetica", 9)
            
        pdf.drawString(60, 710, "Presentamos nuestra oferta de Seguro de Accidentes Personales, la cual cuenta con las siguientes características:")
        altura_solicitante = 685
        altura_suma = 672
        altura_nacimiento = 659
        altura_edad = 646
        altura_genero = 633
        
        altura_cobertura = 582
        altura_accidental = 569
        altura_ITP = 556
        altura_Renta = 530
        altura_Reembolso = 504
        altura_gastos = 491
        altura_total = 478
        pdf.drawString(50, altura_solicitante, "SOLICITANTE:")
        pdf.drawString(50, altura_suma, "SUMA ASEGURADA:")
        pdf.drawString(50, altura_nacimiento, "FECHA DE NACIMIENTO:")
        pdf.drawString(50, altura_edad, "EDAD:")
        pdf.drawString(50, altura_genero, "GÉNERO:")
        pdf.drawString(50, altura_cobertura, "COBERTURAS:")
        pdf.drawString(50, altura_accidental, "MUERTE ACCIDENTAL:")
        pdf.drawString(50, altura_ITP, "INCAPACIDAD TOTAL Y PERMANENTE")
        pdf.drawString(50, altura_ITP-13, "Y PÉRDIDA DE MIEMBROS:")
        pdf.drawString(50, altura_Renta, "RENTA DIARIA POR INCAPACIDAD")
        pdf.drawString(50, altura_Renta-13, "TEMPORAL:")
        pdf.drawString(50, altura_Reembolso, "REEMBOLSO DE GASTOS MÉDICOS")
        pdf.drawString(50, altura_gastos, "GASTOS FUNERARIOS")
        pdf.drawString(50, altura_total, "TOTAL")
        #SOLICITANTE
        ancho_texto1 = pdf.stringWidth(Solicitante, "Helvetica-Bold", 9)
        x_centro1 = 280 + (270 - ancho_texto1)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_solicitante, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x_centro1, altura_solicitante+3, Solicitante)
        pdf.setFont("Helvetica", 9)
        #SUMA ASEGURADA
        if Suma == "$25,000":
            suma = 25000
        elif Suma == "$50,000":
            suma = 50000
        elif Suma == "$100,000":
            suma = 100000
        elif Suma == "$150,000":
            suma = 150000
        elif Suma == "$250,000":
            suma = 250000
        else:
            suma = 500000
        SumaAsegurada = "{:,.2f}".format(float(suma))
        ancho_texto2 = pdf.stringWidth(SumaAsegurada, "Helvetica", 9)
        x_centro2 = 280 + (270 - ancho_texto2)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_suma, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro2, altura_suma+2, "$" + SumaAsegurada)
        #FECHA DE NACIMIENTO
        ancho_texto3 = pdf.stringWidth(Nacimiento, "Helvetica", 9)
        x_centro3 = 280 + (270 - ancho_texto3)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_nacimiento, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro3, altura_nacimiento+3, Nacimiento)
        #EDAD
        fecha_nacimiento = datetime.strptime(Nacimiento, "%Y/%m/%d")
        fechaActual = datetime.now()
        edad = fechaActual.year - fecha_nacimiento.year - ((fechaActual.month, fechaActual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        ancho_texto4 = pdf.stringWidth(str(edad), "Helvetica", 9)
        x_centro4 = 280 + (270 - ancho_texto4)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_edad, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro4-10, altura_edad+2, str(edad) + " años")
        #GÉNERO
        ancho_text1 = pdf.stringWidth(Genero, "Helvetica", 9)
        x_center1 = 280 + (270 - ancho_text1)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_genero, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_center1, altura_genero+3, Genero)
        #COBERTURAS
        pdf.setFont("Helvetica-Bold", 9)
        ancho_texto6 = pdf.stringWidth("SUMA ASEGURADA", "Helvetica", 9)
        x_centro6 = 280 + (270 - ancho_texto6)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_cobertura, 120, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro6-76, altura_cobertura+3, "SUMA ASEGURADA:")

        ancho_texto7 = pdf.stringWidth("PRIMA", "Helvetica", 9)
        x_centro7 = 280 + (270 - ancho_texto7)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(450, altura_cobertura, 100, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro7+85, altura_cobertura+3, "PRIMA:")
        #MUERTE ACCIDENTAL
        if Tip == "A":
            r_riesgo = 0
        elif Tip == "B":
            r_riesgo = 0.15
        else:
            r_riesgo = 0.30
        
        Suma1 = "{:,.2f}".format(float(suma))
        pdf.setFont("Helvetica", 9)
        ancho_texto8 = pdf.stringWidth("$"+ Suma1, "Helvetica", 9)
        x_centro8 = 280 + (120 - ancho_texto8)/2
        pdf.drawString(x_centro8, altura_accidental, "$" + Suma1)
        edadP = int(edad)
        SumaP = int(suma)

        tr_value = TR2.objects.get(Age=edadP).CD

        tr_decimal = Decimal(tr_value)
        PrimaP = (((tr_decimal * Decimal(0.5)) * SumaP)/Decimal(0.5)) * Decimal(1 + r_riesgo)
        
        PrimaP1 = "{:,.2f}".format(float(PrimaP))
        ancho_texto9 = pdf.stringWidth("$" + str(PrimaP1), "Helvetica", 9)
        x_centro9 = 450 + (100 - ancho_texto9)/2
        pdf.drawString(x_centro9, altura_accidental, "$" + str(PrimaP1))
        #ITP
        if Bene == 'Si':
            ancho_texto14 = pdf.stringWidth("$" +  str(Suma1), "Helvetica", 9)
            x_centro14 = 280 + (120 - ancho_texto14)/2
            pdf.drawString(x_centro14, altura_ITP-13+1, "$" + str(Suma1))
        else:
            ancho_texto14 = pdf.stringWidth("", "Helvetica", 9)
            x_centro14 = 280 + (120 - ancho_texto14)/2
            pdf.drawString(x_centro14, altura_ITP-13, "")
        PrimaITP = 0
        if Bene == 'Si':
            PrimaITP = ((0.000312771896557581 * float(SumaP))/0.5) * (1+ r_riesgo)
            PrimaITP1 = "{:,.2f}".format(float(PrimaITP))
            ancho_texto15 = pdf.stringWidth("$" + str(PrimaITP1), "Helvetica", 9)
            x_centro15 = 450 + (100 - ancho_texto15)/2
            pdf.drawString(x_centro15, altura_ITP-13+1, "$" + str(PrimaITP1))
        else:
            PrimaITP1 = "{:,.2f}".format(float(PrimaITP))
            ancho_texto15 = pdf.stringWidth("", "Helvetica", 9)
            x_centro15 = 450 + (100 - ancho_texto15)/2
            pdf.drawString(x_centro15, altura_ITP-13+1, "")
        #RENTA DIARIA POR INCAPACIDAD TEMPORAL
        if Bene == 'Si':
            ancho_txt14 = pdf.stringWidth("$4,500.00", "Helvetica", 9)
            x_ctr14 = 280 + (120 - ancho_txt14)/2
            pdf.drawString(x_ctr14, altura_Renta-13+1, "$4,500.00")
        else:
            ancho_txt14 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr14 = 280 + (120 - ancho_txt14)/2
            pdf.drawString(x_ctr14, altura_Renta-13, "")
        PrimaRenta = 0
        if Bene == 'Si':
            PrimaRenta = ((0.001563859482787910 * 4500)/0.5) * (1 + r_riesgo)
            PrimaRenta1 = "{:,.2f}".format(float(PrimaRenta))
            ancho_txt15 = pdf.stringWidth("$" + str(PrimaRenta1), "Helvetica", 9)
            x_ctr15 = 450 + (100 - ancho_txt15)/2
            pdf.drawString(x_ctr15, altura_Renta-13+1, "$" + str(PrimaRenta1))
        else:
            PrimaRenta1 = "{:,.2f}".format(float(PrimaRenta))
            ancho_txt15 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr15 = 450 + (100 - ancho_txt15)/2
            pdf.drawString(x_ctr15, altura_Renta-13+1, "")
        #REEMBOLSO DE GASTOS MÉDICOS
        if Bene == 'Si':
            ancho_txt18 = pdf.stringWidth("$3,000.00", "Helvetica", 9)
            x_ctr18 = 280 + (120 - ancho_txt18)/2
            pdf.drawString(x_ctr18, altura_Reembolso+1, "$3,000.00")
        else:
            ancho_txt18 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr18 = 280 + (120 - ancho_txt18)/2
            pdf.drawString(x_ctr14, altura_Reembolso, "")
        PrimaReembolso = 0
        if Bene == 'Si':
            PrimaReembolso = ((0.004087494934363430 * 3000)/0.5) * (1 + r_riesgo)
            PrimaReembolso1 = "{:,.2f}".format(float(PrimaReembolso))
            ancho_txt18 = pdf.stringWidth("$" + str(PrimaReembolso1), "Helvetica", 9)
            x_ctr18 = 450 + (100 - ancho_txt18)/2
            pdf.drawString(x_ctr18, altura_Reembolso+1, "$" + str(PrimaReembolso1))
        else:
            PrimaReembolso1 = "{:,.2f}".format(float(PrimaReembolso))
            ancho_txt18 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr18 = 450 + (100 - ancho_txt18)/2
            pdf.drawString(x_ctr18, altura_Reembolso+1, "")
        #GASTOS FUNERARIOS
        if Bene == 'Si':
            ancho_txt19 = pdf.stringWidth("$2,500.00", "Helvetica", 9)
            x_ctr19 = 280 + (120 - ancho_txt19)/2
            pdf.drawString(x_ctr19, altura_gastos+1, "$2,500.00")
        else:
            ancho_txt19 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr19 = 280 + (120 - ancho_txt19)/2
            pdf.drawString(x_ctr19, altura_gastos, "")
        PrimaGastos = 0
        if Bene == 'Si':
            PrimaGastos = (((tr_decimal * Decimal(0.5)) * (2500))/Decimal(0.5)) * Decimal(1 + r_riesgo)
            PrimaGastos1 = "{:,.2f}".format(float(PrimaGastos))
            ancho_txt20 = pdf.stringWidth("$" + str(PrimaGastos1), "Helvetica", 9)
            x_ctr20 = 450 + (100 - ancho_txt20)/2
            pdf.drawString(x_ctr20, altura_gastos+1, "$" + str(PrimaGastos1))
        else:
            PrimaGastos1 = "{:,.2f}".format(float(PrimaGastos))
            ancho_txt20 = pdf.stringWidth("", "Helvetica", 9)
            x_ctr20 = 450 + (100 - ancho_txt20)/2
            pdf.drawString(x_ctr20, altura_gastos+1, "")
        #TOTAL
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_total-5, 120, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)

        PrimaTotal = float(PrimaP) + float(PrimaITP) + float(PrimaRenta) + float(PrimaReembolso) + float(PrimaGastos)
        PrimaTotal1 = "{:,.2f}".format(float(PrimaTotal))
        ancho_texto16 = pdf.stringWidth("$" + str(PrimaTotal1), "Helvetica", 9)
        x_centro16 = 450 + (100 - ancho_texto16)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(450, altura_total-5, 100, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x_centro16, altura_total-2, "$" + str(PrimaTotal1))
        pdf.setFont("Helvetica", 9)

        PrimaTotal = float(PrimaTotal)
        PrimaTotal1 = "{:,.2f}".format(float(PrimaTotal))
        #FORMA DE PAGO
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 456, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(270, 460, "FORMA DE PAGO:")
        pdf.setFont("Helvetica", 9)
        #ANUAL
        pdf.drawString(120, 444, "ANUAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(170, 441, 15, 12, fill=False, stroke=True)
        #SEMESTRAL
        pdf.drawString(200, 444, "SEMESTRAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(270, 441, 15, 12, fill=False, stroke=True)
        #TRIMESTRAL
        pdf.drawString(300, 444, "TRIMESTRAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(370, 441, 15, 12, fill=False, stroke=True)
        #MENSUAL
        pdf.drawString(400, 444, "MENSUAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(460, 441, 15, 12, fill=False, stroke=True)
        #FORMA DE PAGO2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 422, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(210, 428, "FORMA DE PAGO (Incluye gastos e impuestos)")
        pdf.setFont("Helvetica", 9)
        #PARÁMETROS DE FORMAS DE PAGO2
        #ANUAL
        parametro1 = "ANUAL:          1 cuota anual de $" + str(PrimaTotal1) + " al suscribir el Seguro." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 414, 497, 11, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 415, parametro1)
        #SEMESTRAL
        PrimaTotalSemestral = (float(PrimaTotal) * 1.04)/2
        PrimaTotalSemestral = "{:,.2f}".format(float(PrimaTotalSemestral))
        parametro2 = "SEMESTRAL: 1 cuota de $" + str(PrimaTotalSemestral) + " al suscribir el Seguro y $" + str(PrimaTotalSemestral) + " el semestre siguiente." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 402, 497, 12, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 402, parametro2)
        #TRIMESTRAL
        PrimaTotalTrimestral = (float(PrimaTotal) * 1.06)/4
        PrimaTotalTrimestral = "{:,.2f}".format(float(PrimaTotalTrimestral))
        parametro3 = "TRIMESTRAL:1 cuota de $" + str(PrimaTotalTrimestral) + " al suscribir el Seguro y $" + str(PrimaTotalTrimestral) + " cada uno de los trimestres siguientes." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 390, 497, 11, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 390, parametro3)
        #MENSUAL
        PrimaTotalMensual = (float(PrimaTotal) * 1.07)/12
        PrimaTotalMensual = "{:,.2f}".format(float(PrimaTotalMensual))
        parametro4 = "MENSUAL:     1 cuota de $" + str(PrimaTotalMensual) + " al suscribir el Seguro y $" + str(PrimaTotalMensual) + " cada uno de los meses siguientes." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 377, 497, 12, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 377, parametro4)
        #TEXTO DE PRIMA SUJETA A VERIFICACIÓN
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(170, 362, "Prima sujeta a verificación de exámen médico y análisis de suscripción")
        pdf.setFont("Helvetica", 9)
        #TEXTO ABAJO
        pdf.drawString(50, 342, "Si usted acepta la presente cotización, favor devolver los siguientes documentos completos y firmados:")
        pdf.drawString(50, 327, "1. Solicitud de seguro y declaración de salud.")
        pdf.drawString(50, 315, "2. Ficha Integral.")
        pdf.drawString(50, 303, "3. Declaración Jurada.")
        pdf.drawString(50, 291, "4. Documento de Identidad, Pasaporte o Carnet de Residente.")
        pdf.drawString(50, 261, "Oferta válida 30 días a partir de la fecha de su emisión:")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(275, 261, fecha_actual)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(50, 249, "En caso de ser aceptada la oferta, la vigencia de la póliza será anual una vez puesta en vigor.")
        #FIRMAS
        pdf.drawString(100, 170, "__________________________")
        pdf.drawString(110, 158, "Firma de aceptación cliente")
        pdf.drawString(360, 170, "__________________________")
        pdf.drawString(380, 158, "Fecha de aceptación")
        pdf.drawString(100, 118, "__________________________")
        pdf.drawString(116, 106, "Firma de intermediario")
        #Pie de página
        if Nom == "" and In == "":
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: Oficina Principal, Atlántida Vida S.A. Seguro de Personas")
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        else:
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: " + str(In) + ", " + str(Nom))
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 14, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 16, "Atención al cliente: (503)2283-0800")
        pdf.drawString(332, 16, "Correo electrónico: aseguradoatlantida@seatlan.sv")
        # Guardar el PDF en el buffer
        pdf.showPage()
        pdf.setTitle('OFERTA_DE_SACCIDENTES_PERSONALES.pdf')
        pdf.save()

        # Obtener el contenido del buffer y devolverlo como una respuesta HTTP
        #buffer.seek(0)

        pdf_bytes = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename="Oferta_TemporalRenovable.pdf"'
        #response.write(buffer.read())

        correos = [correo for correo in [Cor, Mails] if correo]  # Filtrar correos válidos

        # Si hay correos válidos, enviar el correo
        if correos:
            enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes)
        
        return render(request, 'Oferta_API.html', 
            {'pdf_base64': pdf_base64,
             'Solicitante': Solicitante,
             })

def enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'henriquezricardo459@gmail.com'
    password = 'omou bfpf amij afcw'  # Recuerda almacenar la contraseña de manera segura
    
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(correos)
    msg['Subject'] = 'Oferta de Seguro de Accidentes Personales Individual'

    cuerpo_mensaje = f"""Información del cliente:
    
- Nombre: {Solicitante}
- Edad: {edad}
- Teléfono: {Cellphones}

Es un placer saludarle. Adjuntamos la oferta del Seguro de Accidentes Personales Individual, así cómo los documentos adicionales necesarios en caso de que acepte nuestra cotización.

Cualquier consulta, no dude en responder a este correo o comunicarse con nosotros al 2283-0800. Quedamos a su disposición para cualquier consulta adicional.

Saludos cordiales

Atentamente,

Seguros Atlántida S.A., de C.V.
    """
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
    # Adjuntar el PDF generado
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_bytes)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='Oferta de Seguro de Accidentes Personales Individual.pdf')
    msg.attach(attachment)

    # Adjuntar otros archivos PDF
    for documento in ['Declaracion_Jurada_Persona_Natural.pdf', 'Solicitud_API.pdf', 'Hoja_de_Vinculacion_Persona_Natural.pdf']:
        with open(os.path.join('cotizadorapi/static', documento), 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=documento)
            msg.attach(attachment)

    # Iniciar la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)