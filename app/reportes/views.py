# -*- coding: utf-8 -*-
from io import BytesIO
import copy
from django.core.urlresolvers import reverse
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from collections import OrderedDict
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect    
from reportlab.lib.pagesizes import letter, landscape
from django.core import serializers
from reportlab.platypus import *
from reportlab.lib.units import cm
from reportlab.lib.styles import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import *
from reportlab.pdfgen import canvas
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate, 
    PageTemplate, 
    Frame    
)
from reportlab.lib import utils
#Importamos settings para poder tener a la mano la ruta de la carpeta media
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from time import gmtime, strftime
import locale
from django.db import connection, connections
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from app.pacientes.models import *
from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend

# Establecemos el locale de nuestro sistema
locale.setlocale(locale.LC_ALL, "")


# Create your views here.
def index_pacientes_atendidos(request):

	if request.method == 'POST':
		fecha_inicio = request.POST['fecha_inicio']
		fecha_final = request.POST['fecha_final']
		return HttpResponseRedirect('/reportes/reporte_pacientes_atendidos/%s/%s' %(fecha_inicio,fecha_final))
	else:
		return render(request, 'reportes/pacientes_atendidos.html')

def index_enfermedades_frecuentes(request):

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_final = request.POST['fecha_final']
        return HttpResponseRedirect('/reportes/reporte_enfermedades_frecuentes/%s/%s' %(fecha_inicio,fecha_final))
    else:
        return render(request, 'reportes/enfermedades_frecuentes.html')

def index_frecuencias_consultas(request):

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_final = request.POST['fecha_final']
        return HttpResponseRedirect('/reportes/reporte_frecuencia_consultas/%s/%s' %(fecha_inicio,fecha_final))
    else:
        return render(request, 'reportes/frecuencias_consultas.html')

class Reporte1(View):

    def get(self,request, *args, **kwargs):

        fech1 = self.kwargs['fecha']
        fech2 = self.kwargs['fecha2']
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        nombre = "Pacientes_atendidos_"+fech1+"_"+fech2
        pdf.setTitle(nombre)
        self.cabecera(request,pdf)
        self.cuerpo(pdf,fech1,fech2)
        self.tabla(pdf,fech1,fech2)
        self.pie(pdf)
        page_num = pdf.getPageNumber()
        if page_num > 10:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(484, 687, str(page_num))
            pdf.drawString(480, 687,u"/")
        else:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(479, 687, str(page_num))
            pdf.drawString(470, 687,u"/")
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response  
     
    def cabecera(self,request,pdf):
        current_user = request.user
        showtime = strftime("%d-%m-%Y", gmtime())
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(130, 747, u"Complejo Educativo República de Corea")
        pdf.drawString(240, 722, u"Clínica Medica") 
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(120, 687, u"Fecha de emisión:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(215, 687, showtime)
        pdf.setFont("Times-Bold", 11)  
        pdf.setFont("Times-Bold", 11) 
        page_num = pdf.getPageNumber()
        pdf.drawString(419, 687, u"Página: ")
        pdf.setFont("Times-Roman", 11)
        if page_num > 10:
            pdf.drawString(456, 687, str(page_num))
        else:
            pdf.drawString(459, 687, str(page_num))
        pdf.line(20,665,580,665)

    def cuerpo(self,pdf,fech1,fech2):

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(210, 610, "Reporte de Pacientes Atendidos")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(175, 560, "Fecha inicial:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(250, 560, fech1)
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(340, 560, "Fecha final:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(405, 560, fech2)
        pdf.setFont("Times-Bold", 11)

    def tabla(self,pdf,fech1,fech2):

            encabezados = ('Expediente', 'Nombre','Grado','Genero','Fecha de Consulta')
            data=[]
            #query2 = Alumno.objects.values('expediente','nombres','grado','genero')
            f1 = datetime.datetime.strptime(fech1, '%d-%m-%Y').strftime('%Y-%m-%d')
            f2 = datetime.datetime.strptime(fech2, '%d-%m-%Y').strftime('%Y-%m-%d')
            query1 = Consulta.objects.filter(fecha_consulta__range=[f1, f2]).order_by('fecha_consulta')
            
            cantidad = len(query1)
            #print cantidad
            for alum in query1:
                expediente = Expediente.objects.get(cod_expediente=alum.cod_expediente)
                #print expediente
                Alumnos = Alumno.objects.get(id=expediente.alumno_id)
                grado = str(Alumnos.grado)+"° Grado"
                if Alumnos.genero == 1:
                    sexo = "Masculino"
                else:
                    sexo = "Femenino"
                if Alumnos.grado ==10:
                    grado = "1° Bachillerato"
                elif Alumnos.grado == 11:
                    grado = "2° Bachillerato"
                elif Alumnos.grado == 12:
                    grado = "3° Bachillerato"     
                data.append([
                    (expediente.cod_expediente),
                    (Alumnos.nombres),
                    (grado),
                    (sexo),
                    (alum.fecha_consulta.strftime('%d-%m-%Y')),
                    ])
            total = [("","","","Total",cantidad)]

           # pxatendidos = [cantidad]
            detalle_orden = Table([encabezados] + data +total,colWidths=[3 * cm, 7 * cm, 3 * cm, 3 * cm, 4 * cm])
            detalle_orden.setStyle(TableStyle(
                [
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('GRID', (0, 0  ), (-1, -1), 1, colors.black), 
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1899B2")),
                    ('ROWBACKGROUNDS',(0,1),(-1,cantidad),[colors.white,colors.lightblue]), 
                ]
            ))
            detalle_orden.wrapOn(pdf, 800, 560)
            detalle_orden.drawOn(pdf, 23, 425)

    def pie(self,pdf):
        pdf.line(20,65,580,65)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(250, 52, u"Clínica Medica")
        pdf.drawString(180, 35, u"Complejo Educativo República de Corea")
        pdf.drawString(155, 18, u"Prados de Venecia tercera etapa diagonal Venecia ")

class Reporte2(View):

    def get(self,request, *args, **kwargs):

        fech1 = self.kwargs['fecha']
        fech2 = self.kwargs['fecha2']
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        nombre = "Enfermedades_Frecuentes_"+fech1+"_"+fech2
        pdf.setTitle(nombre)
        self.cabecera(request,pdf)
        self.cuerpo(pdf,fech1,fech2)
        self.tabla(pdf,fech1,fech2)
        self.pie(pdf)
        page_num = pdf.getPageNumber()
        if page_num > 10:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(484, 687, str(page_num))
            pdf.drawString(480, 687,u"/")
        else:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(479, 687, str(page_num))
            pdf.drawString(470, 687,u"/")
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response  
     
    def cabecera(self,request,pdf):
        current_user = request.user
        showtime = strftime("%d-%m-%Y", gmtime())
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(130, 747, u"Complejo Educativo República de Corea")
        pdf.drawString(240, 722, u"Clínica Medica") 
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(120, 687, u"Fecha de emisión:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(215, 687, showtime)
        pdf.setFont("Times-Bold", 11)  
        pdf.setFont("Times-Bold", 11) 
        page_num = pdf.getPageNumber()
        pdf.drawString(419, 687, u"Página: ")
        pdf.setFont("Times-Roman", 11)
        if page_num > 10:
            pdf.drawString(456, 687, str(page_num))
        else:
            pdf.drawString(459, 687, str(page_num))
        pdf.line(20,665,580,665)

    def cuerpo(self,pdf,fech1,fech2):

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(190, 610, "Reporte de Enfermedades más Frecuentes")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(175, 560, "Fecha inicial:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(250, 560, fech1)
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(340, 560, "Fecha final:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(405, 560, fech2)
        pdf.setFont("Times-Bold", 11)

    def tabla(self,pdf,fech1,fech2):

            encabezados = ('Enfermedad','Frecuencia','Enfermedad','Frecuencia')
            data=[]
            #query2 = Alumno.objects.values('expediente','nombres','grado','genero')
            f1 = datetime.datetime.strptime(fech1, '%d-%m-%Y').strftime('%Y-%m-%d')
            f2 = datetime.datetime.strptime(fech2, '%d-%m-%Y').strftime('%Y-%m-%d')
            Q1 = 0
            Q2 = 0
            Q3 = 0
            Q4 = 0
            Q5 = 0
            Q6 = 0
            Q7 = 0
            Q8 = 0
            Q9 = 0
            Q10 = 0
            query1 = Consulta.objects.filter(fecha_consulta__range=[f1, f2])
            for consulta in query1:
                if consulta.otras_enfermedades != None:
                    Q10 += 1
                for enfermedad in consulta.enfermedades.all():
                    if enfermedad.id == 1:
                        Q1 += 1
                    elif enfermedad.id == 2:
                        Q2 += 1
                    elif enfermedad.id == 3:
                        Q3 += 1
                    elif enfermedad.id == 4:
                        Q4 += 1
                    elif enfermedad.id == 5:
                        Q5 += 1
                    elif enfermedad.id == 6:
                        Q6 += 1
                    elif enfermedad.id == 7:
                        Q7 += 1
                    elif enfermedad.id == 8:
                        Q8 += 1
                    elif enfermedad.id == 9:
                        Q9 += 1
            suma = Q1+Q2+Q3+Q4+Q5+Q6+Q7+Q8+Q9+Q10
            cantidad = str(suma)
            cantidadRegistros = len(query1)

            data.append([("Alergias"),(Q1),("Infección de garganta"),(Q6),])
            data.append([("Catarro"),(Q2),("Infección de Oído"),(Q7),])
            data.append([("Conjuntivitis"),(Q3),("Lesión en la piel"),(Q8),])
            data.append([("Desmayo"),(Q4),("Meningitis"),(Q9),])
            data.append([("Dolor de cabeza"),(Q5),("Otras Enfermedades"),(Q10),])
            total = [("","","Total",cantidad)]
            detalle_orden = Table([encabezados] + data +total,colWidths=[4 * cm, 3 * cm, 4 * cm, 3 * cm])
            detalle_orden.setStyle(TableStyle(
                [
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('GRID', (0, 0  ), (-1, -1), 1, colors.black), 
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1899B2")),
                    ('ROWBACKGROUNDS',(0,1),(-1,5),[colors.white,colors.lightblue]), 
                ]
            ))
            detalle_orden.wrapOn(pdf, 800, 560)
            detalle_orden.drawOn(pdf, 110, 375)

    def pie(self,pdf):
        pdf.line(20,65,580,65)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(250, 52, u"Clínica Medica")
        pdf.drawString(180, 35, u"Complejo Educativo República de Corea")
        pdf.drawString(155, 18, u"Prados de Venecia tercera etapa diagonal Venecia ")


class Reporte3(View):

    def get(self,request, *args, **kwargs):

        fech1 = self.kwargs['fecha']
        fech2 = self.kwargs['fecha2']
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        nombre = "Consultas_Frecuentes_"+fech1+"_"+fech2
        pdf.setTitle(nombre)
        self.cabecera(request,pdf)
        self.cuerpo(pdf,fech1,fech2)
        self.tabla(pdf,fech1,fech2)
        self.pie(pdf)
        page_num = pdf.getPageNumber()
        if page_num > 10:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(484, 687, str(page_num))
            pdf.drawString(480, 687,u"/")
        else:
            pdf.setFont("Times-Roman", 11)
            pdf.drawString(479, 687, str(page_num))
            pdf.drawString(470, 687,u"/")
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response  
     
    def cabecera(self,request,pdf):
        current_user = request.user
        showtime = strftime("%d-%m-%Y", gmtime())
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(130, 747, u"Complejo Educativo República de Corea")
        pdf.drawString(240, 722, u"Clínica Medica") 
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(120, 687, u"Fecha de emisión:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(215, 687, showtime)
        pdf.setFont("Times-Bold", 11)  
        pdf.setFont("Times-Bold", 11) 
        page_num = pdf.getPageNumber()
        pdf.drawString(419, 687, u"Página: ")
        pdf.setFont("Times-Roman", 11)
        if page_num > 10:
            pdf.drawString(456, 687, str(page_num))
        else:
            pdf.drawString(459, 687, str(page_num))
        pdf.line(20,665,580,665)    

    def cuerpo(self,pdf,fech1,fech2):

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(190, 610, "Reporte de Frecuencia de Consultas")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(175, 560, "Fecha inicial:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(250, 560, fech1)
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(340, 560, "Fecha final:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(405, 560, fech2)
        pdf.setFont("Times-Bold", 11)

    def tabla(self,pdf,fech1,fech2):
            encabezados = ('Edad','Frecuencia','Edad','Frecuencia')
            data=[]
            #query2 = Alumno.objects.values('expediente','nombres','grado','genero')
            f1 = datetime.datetime.strptime(fech1, '%d-%m-%Y').strftime('%Y-%m-%d')
            f2 = datetime.datetime.strptime(fech2, '%d-%m-%Y').strftime('%Y-%m-%d')
            Q1_4 = 0
            Q5_6 = 0
            Q7_8 = 0
            Q9_10 = 0
            Q11_12 = 0
            Q13_14 = 0
            Q15_16 = 0
            Q17_18 = 0
            Q19_20 = 0
            Q21 = 0
            query1 = Consulta.objects.filter(fecha_consulta__range=[f1, f2])
            for consulta in query1:
                cod_Exp = Expediente.objects.get(cod_expediente=consulta.cod_expediente)
                alumnos = Alumno.objects.get(id=cod_Exp.alumno_id)
                fecha_nac = alumnos.fecha_nacimiento
                diff = (datetime.date.today() - fecha_nac).days
                years = str(int(diff/365))
                print years
                
                if years == 1 and years == 4:
                    Q1_4 += 1
                elif years == 5 and years == 6:
                    Q5_6 += 1
                elif years == 7 and years == 8:
                    Q7_8 += 1
                elif years == 9 and years == 10:
                    Q9_10 += 1
                elif years == 11 and years == 12:
                    Q11_12 += 1
                elif years == 13 and years == 14:
                    Q13_14 += 1
                elif years == 15 and years == 16:
                    Q15_16 += 1
                elif years == 17 and years == 18:
                    Q17_18 += 1
                elif years == 19 and years == 20:
                    Q19_20 += 1
                elif years >= 21:
                    Q21 += 1
            suma = Q1_4+Q5_6+Q7_8+Q9_10+Q11_12+Q13_14+Q15_16+Q17_18+Q19_20+Q21
            cantidad = str(suma)

            data.append([("1 a 4 años"),(Q1_4),("13 a 14 años"),(Q13_14),])
            data.append([("5 a 6 años"),(Q5_6),("15 a 16 años"),(Q15_16),])
            data.append([("7 a 8 años"),(Q7_8),("17 a 18 años"),(Q17_18),])
            data.append([("9 a 10 años"),(Q9_10),("19 a 20 años"),(Q19_20),])
            data.append([("11 a 12 años"),(Q11_12),("21 o más"),(Q21),])
            total = [("","","Total",cantidad)]
            detalle_orden = Table([encabezados] + data +total, colWidths=[3 * cm, 4 * cm, 4 * cm, 3 * cm,])
            detalle_orden.setStyle(TableStyle(
                [
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('GRID', (0, 0  ), (-1, -1), 1, colors.black), 
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1899B2")),
                    ('ROWBACKGROUNDS',(0,1),(-1,5),[colors.white,colors.lightblue]), 
                ]
            ))
            detalle_orden.wrapOn(pdf, 800, 560)
            detalle_orden.drawOn(pdf, 120, 375)

    def pie(self,pdf):
        pdf.line(20,65,580,65)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(250, 52, u"Clínica Medica")
        pdf.drawString(180, 35, u"Complejo Educativo República de Corea")
        pdf.drawString(155, 18, u"Prados de Venecia tercera etapa diagonal Venecia ")

