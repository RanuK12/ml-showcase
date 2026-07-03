import sys
from datetime import datetime
from fpdf import FPDF


# Public emission factors (kg CO2e)
EMISSION_FACTORS = {
    # Transportation (per km)
    "transport": {
        "car_gasoline": 0.21,      # Average gasoline car
        "car_diesel": 0.17,        # Average diesel car
        "car_electric": 0.05,      # Electric car (avg grid)
        "bus": 0.089,              # Public bus
        "train": 0.041,            # Train/metro
        "plane_short": 0.255,      # Short flights (<500km)
        "plane_long": 0.195,       # Long flights (>500km)
        "motorcycle": 0.113,       # Motorcycle
    },
    # Energy (per kWh or unit)
    "energy": {
        "electricity": 0.475,      # Average grid electricity
        "natural_gas": 2.04,       # Per cubic meter
        "heating_oil": 2.68,       # Per liter
    },
    # Food (per kg)
    "food": {
        "beef": 27.0,
        "pork": 12.1,
        "chicken": 6.9,
        "fish": 6.1,
        "dairy": 3.2,
        "vegetables": 2.0,
        "grains": 1.4,
    },
    # Waste (per kg)
    "waste": {
        "landfill": 0.58,          # Landfill waste
        "recycled": 0.02,          # Recycled waste
        "composted": 0.01,         # Composted waste
    },
}


def calculate_transport_emissions(data: dict) -> float:
    """Calculate transportation emissions in kg CO2e."""
    total = 0.0
    for vehicle, km in data.items():
        if vehicle in EMISSION_FACTORS["transport"]:
            total += EMISSION_FACTORS["transport"][vehicle] * km
    return total


def calculate_energy_emissions(data: dict) -> float:
    """Calculate energy emissions in kg CO2e."""
    total = 0.0
    for source, usage in data.items():
        if source in EMISSION_FACTORS["energy"]:
            total += EMISSION_FACTORS["energy"][source] * usage
    return total


def calculate_food_emissions(data: dict) -> float:
    """Calculate food emissions in kg CO2e."""
    total = 0.0
    for food, kg in data.items():
        if food in EMISSION_FACTORS["food"]:
            total += EMISSION_FACTORS["food"][food] * kg
    return total


def calculate_waste_emissions(data: dict) -> float:
    """Calculate waste emissions in kg CO2e."""
    total = 0.0
    for waste_type, kg in data.items():
        if waste_type in EMISSION_FACTORS["waste"]:
            total += EMISSION_FACTORS["waste"][waste_type] * kg
    return total


def calculate_total_footprint(transport=None, energy=None, food=None, waste=None) -> dict:
    """Calculate total carbon footprint from all categories."""
    transport = transport or {}
    energy = energy or {}
    food = food or {}
    waste = waste or {}

    results = {
        "transport": calculate_transport_emissions(transport),
        "energy": calculate_energy_emissions(energy),
        "food": calculate_food_emissions(food),
        "waste": calculate_waste_emissions(waste),
        "transport_details": transport,
        "energy_details": energy,
        "food_details": food,
        "waste_details": waste,
    }
    results["total"] = sum([
        results["transport"],
        results["energy"],
        results["food"],
        results["waste"],
    ])
    return results


def generate_pdf_report(results: dict, filename: str = "carbon_report.pdf", user_name: str = "User"):
    """Generate a PDF report with carbon footprint results."""

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, "Carbon Footprint Report", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 8, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

        def section_title(self, title):
            self.set_font("Helvetica", "B", 13)
            self.set_fill_color(44, 62, 80)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(3)

        def add_table_row(self, col1, col2, col3, bold=False):
            style = "B" if bold else ""
            self.set_font("Helvetica", style, 10)
            self.cell(90, 8, str(col1), border=1)
            self.cell(50, 8, str(col2), border=1, align="R")
            self.cell(50, 8, str(col3), border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Summary section
    pdf.section_title("Summary")
    total = results["total"]
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 10, f"Dear {user_name},", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Your estimated annual carbon footprint is:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(192, 57, 43)
    pdf.cell(0, 15, f"{total:,.2f} kg CO2e", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Helvetica", "", 11)
    equivalent_tonnes = total / 1000
    pdf.cell(0, 10, f"Equivalent to {equivalent_tonnes:,.2f} tonnes CO2e", align="C", new_x="LMARGIN", new_y="NEXT")

    # Comparison with global average
    global_avg = 4700  # kg CO2e per year global average
    if total > global_avg:
        comparison = f"{((total / global_avg) - 1) * 100:.1f}% above"
        color = (192, 57, 43)
    else:
        comparison = f"{(1 - (total / global_avg)) * 100:.1f}% below"
        color = (39, 174, 96)

    pdf.set_text_color(*color)
    pdf.cell(0, 10, f"This is {comparison} the global average ({global_avg:,} kg CO2e/year)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # Category breakdown
    pdf.section_title("Emissions by Category")
    pdf.add_table_row("Category", "Emissions (kg CO2e)", "Percentage", bold=True)

    categories = [
        ("Transportation", results["transport"]),
        ("Energy", results["energy"]),
        ("Food", results["food"]),
        ("Waste", results["waste"]),
    ]
    for name, value in categories:
        pct = (value / total * 100) if total > 0 else 0
        pdf.add_table_row(name, f"{value:,.2f}", f"{pct:.1f}%")

    pdf.add_table_row("TOTAL", f"{total:,.2f}", "100%", bold=True)
    pdf.ln(10)

    # Detailed breakdown sections
    detail_sections = [
        ("Transportation Details", results["transport_details"], EMISSION_FACTORS["transport"], "km", "kg CO2e/km"),
        ("Energy Details", results["energy_details"], EMISSION_FACTORS["energy"], "units", "kg CO2e/unit"),
        ("Food Details", results["food_details"], EMISSION_FACTORS["food"], "kg", "kg CO2e/kg"),
        ("Waste Details", results["waste_details"], EMISSION_FACTORS["waste"], "kg", "kg CO2e/kg"),
    ]

    for title, details, factors, unit_label, factor_label in detail_sections:
        if not details:
            continue

        pdf.section_title(title)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(60, 8, "Item", border=1)
        pdf.cell(30, 8, "Amount", border=1, align="R")
        pdf.cell(40, 8, "Factor", border=1, align="R")
        pdf.cell(40, 8, "Emissions", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 10)
        for item, amount in details.items():
            factor = factors.get(item, 0)
            emissions = factor * amount
            item_name = item.replace("_", " ").title()
            pdf.cell(60, 8, item_name, border=1)
            pdf.cell(30, 8, f"{amount:,.1f}", border=1, align="R")
            pdf.cell(40, 8, f"{factor:.3f}", border=1, align="R")
            pdf.cell(40, 8, f"{emissions:,.2f}", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(5)

    # Recommendations section
    pdf.add_page()
    pdf.section_title("Recommendations to Reduce Your Footprint")

    recommendations = [
        "Use public transportation, bike, or walk when possible",
        "Switch to renewable energy sources for your home",
        "Reduce meat consumption, especially beef",
        "Improve home insulation to reduce heating/cooling needs",
        "Recycle and compost waste properly",
        "Choose local and seasonal products",
        "Reduce air travel and offset emissions when flying",
        "Use energy-efficient appliances",
    ]

    pdf.set_font("Helvetica", "", 11)
    for i, rec in enumerate(recommendations, 1):
        pdf.cell(10, 8, f"{i}.")
        pdf.cell(0, 8, rec, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)

    # Data sources
    pdf.section_title("Data Sources")
    pdf.set_font("Helvetica", "", 9)
    sources = [
        "EPA - US Environmental Protection Agency",
        "DEFRA - UK Department for Environment, Food & Rural Affairs",
        "IPCC - Intergovernmental Panel on Climate Change",
        "IEA - International Energy Agency",
        "Our World in Data - CO2 and Greenhouse Gas Emissions",
    ]
    for source in sources:
        pdf.cell(0, 6, f"• {source}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(filename)
    return filename


# Example usage
if __name__ == "__main__":
    # Example: Calculate footprint for a sample user
    example_results = calculate_total_footprint(
        transport={
            "car_gasoline": 15000,   # 15,000 km per year
            "plane_short": 2000,     # 2,000 km of short flights
            "train": 3000,           # 3,000 km by train
        },
        energy={
            "electricity": 4000,     # 4,000 kWh per year
            "natural_gas": 1200,     # 1,200 cubic meters per year
        },
        food={
            "beef": 30,              # 30 kg per year
            "chicken": 40,           # 40 kg per year
            "dairy": 100,            # 100 kg per year
            "vegetables": 200,       # 200 kg per year
            "grains": 150,           # 150 kg per year
        },
        waste={
            "landfill": 200,         # 200 kg landfill waste
            "recycled": 100,         # 100 kg recycled
            "composted": 50,         # 50 kg composted
        },
    )

    report_file = generate_pdf_report(
        example_results,
        filename="carbon_report.pdf",
        user_name="John Doe"
    )
    print(f"Carbon footprint report generated: {report_file}")
    print(f"Total emissions: {example_results['total']:,.2f} kg CO2e")
