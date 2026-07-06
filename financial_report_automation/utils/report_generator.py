import pandas as pd
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_excel_report(self, data, report_name):
        """Generar informe en Excel."""
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{report_name}_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        return filename

    def generate_csv_report(self, data, report_name):
        """Generar informe en CSV."""
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{report_name}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        return filename

    def generate_pdf_report(self, data, report_name):
        """Generar informe en PDF (usando reportlab)."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{report_name}_{timestamp}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Convertir datos a tabla
        df = pd.DataFrame(data)
        data_table = [df.columns.tolist()] + df.values.tolist()
        table = Table(data_table)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        doc.build(elements)
        return filename