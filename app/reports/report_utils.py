from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import io
from decimal import Decimal

class ReportUtils:
    """Utilidades para generar reportes PDF con ReportLab"""
    
    @staticmethod
    def generar_recibo_salario(empleado, liquidacion):
        """
        Genera un recibo de salario en PDF
        
        Args:
            empleado: Objeto Empleado
            liquidacion: Objeto Liquidacion
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("RECIBO DE SALARIO", title_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Información general
        info_data = [
            ['Periodo:', liquidacion.periodo, 'Fecha de Emisión:', datetime.now().strftime('%d/%m/%Y')],
            ['Empleado:', empleado.nombre_completo, 'Código:', empleado.codigo],
            ['CI:', empleado.ci, 'Cargo:', empleado.cargo.nombre],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Detalles de liquidación
        detail_data = [
            ['CONCEPTO', 'VALOR'],
            ['Salario Base', f"₲ {float(liquidacion.salario_base):,.2f}"],
            ['Ingresos Extras', f"₲ {float(liquidacion.ingresos_extras):,.2f}"],
            ['Subtotal Ingresos', f"₲ {float(liquidacion.salario_base + liquidacion.ingresos_extras):,.2f}"],
            ['', ''],
            ['Descuentos', f"₲ {float(liquidacion.descuentos):,.2f}"],
            ['Aporte IPS (9.625%)', f"₲ {float(liquidacion.aporte_ips):,.2f}"],
            ['Total Descuentos', f"₲ {float(liquidacion.descuentos + liquidacion.aporte_ips):,.2f}"],
            ['', ''],
            ['SALARIO NETO', f"₲ {float(liquidacion.salario_neto):,.2f}"],
        ]
        
        detail_table = Table(detail_data, colWidths=[4*inch, 2*inch])
        detail_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(detail_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Nota
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Este recibo fue generado automáticamente por el sistema de RRHH", note_style))
        story.append(Paragraph(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", note_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_planilla_mensual(empleados_liquidaciones, periodo):
        """
        Genera planilla consolidada mensual
        
        Args:
            empleados_liquidaciones: Lista de tuplas (empleado, liquidacion)
            periodo: String con formato YYYY-MM
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.3*inch, leftMargin=0.3*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("PLANILLA DE LIQUIDACIÓN DE SALARIOS", title_style))
        story.append(Paragraph(f"Período: {periodo}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Tabla de datos
        data = [['Código', 'Empleado', 'Cargo', 'Salario Base', 'Ingresos', 'Descuentos', 'IPS', 'Salario Neto']]
        
        total_salario_base = Decimal('0')
        total_ingresos = Decimal('0')
        total_descuentos = Decimal('0')
        total_ips = Decimal('0')
        total_neto = Decimal('0')
        
        for empleado, liquidacion in empleados_liquidaciones:
            data.append([
                empleado.codigo,
                empleado.nombre_completo,
                empleado.cargo.nombre,
                f"₲ {float(liquidacion.salario_base):,.0f}",
                f"₲ {float(liquidacion.ingresos_extras):,.0f}",
                f"₲ {float(liquidacion.descuentos):,.0f}",
                f"₲ {float(liquidacion.aporte_ips):,.0f}",
                f"₲ {float(liquidacion.salario_neto):,.0f}",
            ])
            
            total_salario_base += liquidacion.salario_base
            total_ingresos += liquidacion.ingresos_extras
            total_descuentos += liquidacion.descuentos
            total_ips += liquidacion.aporte_ips
            total_neto += liquidacion.salario_neto
        
        # Fila de totales
        data.append([
            '',
            'TOTAL',
            '',
            f"₲ {float(total_salario_base):,.0f}",
            f"₲ {float(total_ingresos):,.0f}",
            f"₲ {float(total_descuentos):,.0f}",
            f"₲ {float(total_ips):,.0f}",
            f"₲ {float(total_neto):,.0f}",
        ])
        
        table = Table(data, colWidths=[0.9*inch, 2.2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
            ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Resumen
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=7,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", note_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_contrato_pdf(empleado, cargo, fecha_inicio, fecha_fin=None):
        """
        Genera un contrato de trabajo en PDF
        
        Args:
            empleado: Objeto Empleado
            cargo: Objeto Cargo
            fecha_inicio: Fecha de inicio del contrato
            fecha_fin: Fecha de fin del contrato (opcional)
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("CONTRATO DE TRABAJO", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Cuerpo del contrato
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        fecha_inicio_str = fecha_inicio.strftime('%d de %B de %Y') if hasattr(fecha_inicio, 'strftime') else str(fecha_inicio)
        
        contenido = f"""
        <b>ENTRE:</b><br/>
        El suscrito COOPERATIVA RRHH, por una parte, y {empleado.nombre_completo}, 
        portador de Cédula de Identidad Nº {empleado.ci}, mayor de edad, capaz según la ley, 
        por la otra parte, acuerdan celebrar el presente Contrato de Trabajo bajo los siguientes términos:<br/><br/>
        
        <b>PRIMERO:</b> El empleador contrata al trabajador para que desempeñe las funciones 
        correspondientes al cargo de {cargo.nombre}, con un salario base de ₲ {float(cargo.salario_base):,.2f} mensual.<br/><br/>
        
        <b>SEGUNDO:</b> El presente contrato comenzará a regir desde el {fecha_inicio_str} 
        y durará por tiempo indeterminado, salvo disposición contraria de ambas partes.<br/><br/>
        
        <b>TERCERO:</b> El trabajador se compromete a cumplir con sus obligaciones laborales, 
        acatar la disciplina de la empresa y respetar las normas internas de convivencia.<br/><br/>
        
        <b>CUARTO:</b> El empleador se obliga a pagar el salario en la forma y oportunidad establecida 
        en la ley, así como proporcionar las condiciones de seguridad e higiene en el trabajo.<br/><br/>
        
        Firmado en la ciudad de Asunción, a los {datetime.now().strftime('%d')} días del mes de {datetime.now().strftime('%B')} de {datetime.now().strftime('%Y')}.<br/>
        """
        
        story.append(Paragraph(contenido, body_style))
        story.append(Spacer(1, 0.4*inch))
        
        # Firmas
        firma_style = ParagraphStyle(
            'FirmaStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        story.append(Paragraph("_________________________", firma_style))
        story.append(Paragraph("Empleador", firma_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("_________________________", firma_style))
        story.append(Paragraph(f"{empleado.nombre_completo}", firma_style))
        story.append(Paragraph("Trabajador", firma_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
