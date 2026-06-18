from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_fill_color(26, 26, 46)
        self.rect(0, 0, 210, 20, 'F')
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 212, 255)
        self.cell(0, 10, 'Redbean Quick Start Guide', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Ranukita Bot - Propiedad de Ranuk IT Solutions | ranuk.dev', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.set_text_color(255, 215, 0)
pdf.cell(0, 20, "Welcome to Redbean", 0, 1, "L")

pdf.set_font("Arial", "", 12)
pdf.set_text_color(0, 0, 0)
content = [
    ("Installation", "1. Download the Redbean executable.\n2. Place it in your desired directory.\n3. Ensure you have the necessary permissions to execute the file."),
    ("Running your first page", "1. Create a 'page.lua' file in the same directory.\n2. Run the executable: ./redbean --port 8080\n3. Open your browser at http://localhost:8080"),
    ("Customization", "Redbean uses Lua for logic and SQLite for data persistence. You can modify the page.lua file to change content, handle forms, or query the database directly."),
    ("Deployment", "Since Redbean is a single file, you can ship it directly to your clients or host it on any server with minimal overhead.")
]

for title, text in content:
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, text)

pdf.output("/Users/emilioranucoli/Desktop/Oficina_Ranuk/Redbean_QuickStart_Guide.pdf")
