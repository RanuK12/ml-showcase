import sys
from datetime import datetime
from fpdf import FPDF
from typing import Optional


# Public emission factors (kg CO2e)
# Sources:
# - EPA (US Environmental Protection Agency)
# - DEFRA (UK Department for Environment, Food & Rural Affairs)
# - IPCC (Intergovernmental Panel on Climate Change)
# - IEA (International Energy Agency)
EMISSION_FACTORS = {
    # Transportation (per km)
    "transport": {
        "car_gasoline": 0.21,      # Average gasoline car
        "car_diesel": 0.17,        # Average diesel car
        "car_electric": 0.05,      # Electric car (avg grid)
        "hybrid": 0.12,            # Hybrid vehicle
        "bus": 0.089,              # Public bus
        "train": 0.041,            # Train/metro
        "plane_short": 0.255,      # Short flights (<500km)
        "plane_long": 0.195,       # Long flights (>500km)
        "motorcycle": 0.113,       # Motorcycle
        "bicycle": 0.0,            # Bicycle (zero emissions)
        "walking": 0.0,            # Walking (zero emissions)
    },
    # Energy (per kWh or unit)
    "energy": {
        "electricity": 0.475,      # Average grid electricity (kWh)
        "natural_gas": 2.04,       # Per cubic meter
        "heating_oil": 2.68,       # Per liter
        "propane": 1.51,           # Per liter
        "wood": 0.39,              # Per kg (sustainable source)
    },
    # Food (per kg)
    "food": {
        "beef": 27.0,
        "lamb": 24.0,
        "pork": 12.1,
        "chicken": 6.9,
        "turkey": 5.8,
        "fish": 6.1,
        "seafood": 7.5,
        "dairy": 3.2,
        "eggs": 4.8,
        "vegetables": 2.0,
        "fruits": 1.5,
        "grains": 1.4,
        "legumes": 0.9,
        "nuts": 0.3,
    },
    # Waste (per kg)
    "waste": {
        "landfill": 0.58,          # Landfill waste
        "recycled": 0.02,          # Recycled waste
        "composted": 0.01,         # Composted waste
        "incinerated": 0.45,       # Incinerated waste
    },
    # Water (per cubic meter)
    "water": {
        "tap_water": 0.298,        # Municipal water supply
        "hot_water": 0.596,        # Heated water
    },
}

# Global and regional averages for comparison (kg CO2e per year)
COMPARISON_BENCHMARKS = {
    "global_average": 4700,
    "us_average": 16000,
    "eu_average": 6800,
    "china_average": 8000,
    "india_average": 1900,
    "target_2030": 2300,           # Paris Agreement target
    "target_2050": 1000,           # Net-zero pathway target
}


def validate_input(data: dict, category: str) -> bool:
    """Validate input data for emissions calculations."""
    if not isinstance(data, dict):
        raise ValueError(f"{category} data must be a dictionary")
    
    valid_keys = EMISSION_FACTORS.get(category, {})
    for key in data.keys():
        if key not in valid_keys:
            print(f"Warning: Unknown {category} factor '{key}' - will be ignored")
        if not isinstance(data[key], (int, float)):
            raise ValueError(f"Value for '{key}' must be numeric, got {type(data[key])}")
        if data[key] < 0:
            raise ValueError(f"Value for '{key}' cannot be negative")
    
    return True


def calculate_transport_emissions(data: dict) -> float:
    """Calculate transportation emissions in kg CO2e.
    
    Args:
        data: Dictionary mapping transport modes to km traveled per year
        
    Returns:
        Total transport emissions in kg CO2e
    """
    if not data:
        return 0.0
    validate_input(data, "transport")
    
    total = 0.0
    for vehicle, km in data.items():
        if vehicle in EMISSION_FACTORS["transport"]:
            factor = EMISSION_FACTORS["transport"][vehicle]
            emissions = factor * km
            total += emissions
    return total


def calculate_energy_emissions(data: dict) -> float:
    """Calculate energy emissions in kg CO2e.
    
    Args:
        data: Dictionary mapping energy sources to usage amounts
        
    Returns:
        Total energy emissions in kg CO2e
    """
    if not data:
        return 0.0
    validate_input(data, "energy")
    
    total = 0.0
    for source, usage in data.items():
        if source in EMISSION_FACTORS["energy"]:
            factor = EMISSION_FACTORS["energy"][source]
            emissions = factor * usage
            total += emissions
    return total


def calculate_food_emissions(data: dict) -> float:
    """Calculate food emissions in kg CO2e.
    
    Args:
        data: Dictionary mapping food types to kg consumed per year
        
    Returns:
        Total food emissions in kg CO2e
    """
    if not data:
        return 0.0
    validate_input(data, "food")
    
    total = 0.0
    for food, kg in data.items():
        if food in EMISSION_FACTORS["food"]:
            factor = EMISSION_FACTORS["food"][food]
            emissions = factor * kg
            total += emissions
    return total


def calculate_waste_emissions(data: dict) -> float:
    """Calculate waste emissions in kg CO2e.
    
    Args:
        data: Dictionary mapping waste types to kg per year
        
    Returns:
        Total waste emissions in kg CO2e
    """
    if not data:
        return 0.0
    validate_input(data, "waste")
    
    total = 0.0
    for waste_type, kg in data.items():
        if waste_type in EMISSION_FACTORS["waste"]:
            factor = EMISSION_FACTORS["waste"][waste_type]
            emissions = factor * kg
            total += emissions
    return total


def calculate_water_emissions(data: dict) -> float:
    """Calculate water-related emissions in kg CO2e.
    
    Args:
        data: Dictionary mapping water types to cubic meters used per year
        
    Returns:
        Total water emissions in kg CO2e
    """
    if not data:
        return 0.0
    validate_input(data, "water")
    
    total = 0.0
    for water_type, volume in data.items():
        if water_type in EMISSION_FACTORS["water"]:
            factor = EMISSION_FACTORS["water"][water_type]
            emissions = factor * volume
            total += emissions
    return total


def calculate_total_footprint(
    transport: Optional[dict] = None,
    energy: Optional[dict] = None,
    food: Optional[dict] = None,
    waste: Optional[dict] = None,
    water: Optional[dict] = None
) -> dict:
    """Calculate total carbon footprint from all categories.
    
    Args:
        transport: Transportation data (km per year by mode)
        energy: Energy usage data (kWh, cubic meters, liters)
        food: Food consumption data (kg per year)
        waste: Waste generation data (kg per year)
        water: Water usage data (cubic meters per year)
        
    Returns:
        Dictionary with emissions breakdown and totals
    """
    transport = transport or {}
    energy = energy or {}
    food = food or {}
    waste = waste or {}
    water = water or {}

    transport_emissions = calculate_transport_emissions(transport)
    energy_emissions = calculate_energy_emissions(energy)
    food_emissions = calculate_food_emissions(food)
    waste_emissions = calculate_waste_emissions(waste)
    water_emissions = calculate_water_emissions(water)

    results = {
        "transport": transport_emissions,
        "energy": energy_emissions,
        "food": food_emissions,
        "waste": waste_emissions,
        "water": water_emissions,
        "transport_details": transport,
        "energy_details": energy,
        "food_details": food,
        "waste_details": waste,
        "water_details": water,
        "generated_at": datetime.now().isoformat(),
    }
    
    results["total"] = sum([
        results["transport"],
        results["energy"],
        results["food"],
        results["waste"],
        results["water"],
    ])
    
    # Calculate percentages
    if results["total"] > 0:
        results["percentages"] = {
            "transport": (results["transport"] / results["total"]) * 100,
            "energy": (results["energy"] / results["total"]) * 100,
            "food": (results["food"] / results["total"]) * 100,
            "waste": (results["waste"] / results["total"]) * 100,
            "water": (results["water"] / results["total"]) * 100,
        }
    else:
        results["percentages"] = {
            "transport": 0,
            "energy": 0,
            "food": 0,
            "waste": 0,
            "water": 0,
        }
    
    return results


def get_comparison(total_emissions: float) -> dict:
    """Compare emissions against various benchmarks.
    
    Args:
        total_emissions: Total emissions in kg CO2e
        
    Returns:
        Dictionary with comparison data
    """
    comparisons = {}
    for benchmark_name, benchmark_value in COMPARISON_BENCHMARKS.items():
        if total_emissions > benchmark_value:
            diff_pct = ((total_emissions / benchmark_value) - 1) * 100
            comparisons[benchmark_name] = {
                "value": benchmark_value,
                "difference_pct": diff_pct,
                "status": "above",
            }
        else:
            diff_pct = (1 - (total_emissions / benchmark_value)) * 100
            comparisons[benchmark_name] = {
                "value": benchmark_value,
                "difference_pct": diff_pct,
                "status": "below",
            }
    
    return comparisons


def get_recommendations(results: dict) -> list:
    """Generate personalized recommendations based on carbon footprint.
    
    Args:
        results: Carbon footprint calculation results
        
    Returns:
        List of prioritized recommendations
    """
    recommendations = []
    total = results["total"]
    percentages = results["percentages"]
    
    # Transportation recommendations
    if percentages["transport"] > 30:
        transport = results["transport_details"]
        if "car_gasoline" in transport or "car_diesel" in transport:
            recommendations.append({
                "category": "Transport",
                "priority": "High",
                "tip": "Consider switching to an electric or hybrid vehicle to reduce emissions by up to 75%",
            })
        if any(k.startswith("plane") for k in transport.keys()):
            recommendations.append({
                "category": "Transport",
                "priority": "High",
                "tip": "Reduce air travel or purchase carbon offsets for flights",
            })
        recommendations.append({
            "category": "Transport",
            "priority": "Medium",
            "tip": "Use public transportation, cycling, or walking for shorter distances",
        })
    
    # Energy recommendations
    if percentages["energy"] > 25:
        recommendations.append({
            "category": "Energy",
            "priority": "High",
            "tip": "Switch to renewable energy sources or green energy tariffs",
        })
        recommendations.append({
            "category": "Energy",
            "priority": "Medium",
            "tip": "Improve home insulation and use energy-efficient appliances",
        })
    
    # Food recommendations
    if percentages["food"] > 20:
        food = results["food_details"]
        if "beef" in food or "lamb" in food:
            recommendations.append({
                "category": "Food",
                "priority": "High",
                "tip": "Reduce red meat consumption - beef and lamb have the highest carbon footprint",
            })
        recommendations.append({
            "category": "Food",
            "priority": "Medium",
            "tip": "Choose local, seasonal products and reduce food waste",
        })
    
    # Waste recommendations
    if percentages["waste"] > 10:
        waste = results["waste_details"]
        if waste.get("landfill", 0) > waste.get("recycled", 0):
            recommendations.append({
                "category": "Waste",
                "priority": "High",
                "tip": "Increase recycling and composting to divert waste from landfills",
            })
    
    # General recommendations (always included)
    recommendations.extend([
        {"category": "General", "priority": "Low", "tip": "Plant trees or support reforestation projects"},
        {"category": "General", "priority": "Low", "tip": "Support carbon offset programs for unavoidable emissions"},
    ])
    
    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return recommendations


def generate_pdf_report(
    results: dict,
    filename: str = "carbon_report.pdf",
    user_name: str = "User",
    include_recommendations: bool = True
) -> str:
    """Generate a comprehensive PDF report with carbon footprint results.
    
    Args:
        results: Carbon footprint calculation results
        filename: Output PDF filename
        user_name: Name for personalization
        include_recommendations: Whether to include recommendations section
        
    Returns:
        Path to generated PDF file
    """

    class PDF(FPDF):
        def header(self):
            self.set_fill_color(26, 95, 57)  # Dark green
            self.rect(0, 0, 210, 25, 'F')
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(255, 255, 255)
            self.set_y(5)
            self.cell(0, 15, "Carbon Footprint Report", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.set_y(30)

        def footer(self):
            self.set_y(-20)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, f"Generated by CarbonLoop AI | {datetime.now().strftime('%Y-%m-%d')}", align="L", new_x="LMARGIN", new_y="NEXT")
            self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R")
            self.set_text_color(0, 0, 0)

        def section_title(self, title, icon=""):
            self.ln(3)
            self.set_font("Helvetica", "B", 13)
            self.set_fill_color(39, 174, 96)  # Green
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, f"  {icon} {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(4)

        def add_table_row(self, col1, col2, col3, bold=False, header=False):
            style = "B" if bold or header else ""
            if header:
                self.set_fill_color(52, 73, 94)
                self.set_text_color(255, 255, 255)
            elif bold:
                self.set_fill_color(236, 240, 241)
            else:
                self.set_fill_color(255, 255, 255)
            
            self.set_font("Helvetica", style, 10)
            self.cell(80, 8, str(col1), border=1, fill=True)
            self.cell(50, 8, str(col2), border=1, align="R", fill=True)
            self.cell(50, 8, str(col3), border=1, align="R", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)

        def add_detail_row(self, item, amount, factor, emissions, unit=""):
            self.set_font("Helvetica", "", 9)
            self.cell(50, 7, str(item), border=1)
            self.cell(25, 7, str(amount), border=1, align="R")
            self.cell(30, 7, str(factor), border=1, align="R")
            self.cell(35, 7, str(emissions), border=1, align="R")
            self.cell(30, 7, str(unit), border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Personal greeting
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Dear {user_name},", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Here is your personalized carbon footprint analysis:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Total emissions highlight
    total = results["total"]
    equivalent_tonnes = total / 1000
    
    pdf.set_fill_color(231, 76, 60)  # Red background for impact
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "  YOUR ANNUAL CARBON FOOTPRINT", fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_fill_color(192, 57, 43)
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 20, f"  {total:,.2f} kg CO2e", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, f"  Equivalent to {equivalent_tonnes:,.2f} tonnes CO2e", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)

    # Comparison with benchmarks
    comparisons = get_comparison(total)
    
    pdf.section_title("Comparison with Averages", "📊")
    pdf.add_table_row("Benchmark", "Average (kg)", "Your Status", header=True)
    
    display_benchmarks = ["global_average", "us_average", "eu_average", "target_2030"]
    for benchmark in display_benchmarks:
        comp = comparisons[benchmark]
        label = benchmark.replace("_", " ").title()
        if comp["status"] == "above":
            status = f"+{comp['difference_pct']:.1f}% above"
            pdf.set_text_color(192, 57, 43)  # Red
        else:
            status = f"-{comp['difference_pct']:.1f}% below"
            pdf.set_text_color(39, 174, 96)  # Green
        pdf.add_table_row(label, f"{comp['value']:,}", status)
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)

    # Category breakdown
    pdf.section_title("Emissions by Category", "📁")
    pdf.add_table_row("Category", "Emissions (kg CO2e)", "Percentage", header=True)

    categories = [
        ("Transportation", results["transport"]),
        ("Energy", results["energy"]),
        ("Food", results["food"]),
        ("Waste", results["waste"]),
        ("Water", results["water"]),
    ]
    for name, value in categories:
        pct = (value / total * 100) if total > 0 else 0
        pdf.add_table_row(name, f"{value:,.2f}", f"{pct:.1f}%")

    pdf.add_table_row("TOTAL", f"{total:,.2f}", "100%", bold=True)
    pdf.ln(5)

    # Detailed breakdown sections
    detail_sections = [
        ("Transportation Details", results["transport_details"], EMISSION_FACTORS["transport"], "km/year", "kg CO2e/km"),
        ("Energy Details", results["energy_details"], EMISSION_FACTORS["energy"], "units/year", "kg CO2e/unit"),
        ("Food Details", results["food_details"], EMISSION_FACTORS["food"], "kg/year", "kg CO2e/kg"),
        ("Waste Details", results["waste_details"], EMISSION_FACTORS["waste"], "kg/year", "kg CO2e/kg"),
        ("Water Details", results["water_details"], EMISSION_FACTORS["water"], "m³/year", "kg CO2e/m³"),
    ]

    for title, details, factors, unit_label, factor_label in detail_sections:
        if not details:
            continue

        pdf.section_title(title, "📋")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(52, 73, 94)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(50, 7, "Item", border=1, fill=True)
        pdf.cell(25, 7, "Amount", border=1, align="R", fill=True)
        pdf.cell(30, 7, "Factor", border=1, align="R", fill=True)
        pdf.cell(35, 7, "Emissions", border=1, align="R", fill=True)
        pdf.cell(30, 7, "Unit", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Helvetica", "", 9)
        for item, amount in details.items():
            factor = factors.get(item, 0)
            emissions = factor * amount
            item_name = item.replace("_", " ").title()
            pdf.add_detail_row(item_name, f"{amount:,.1f}", f"{factor:.3f}", f"{emissions:,.2f}", unit_label)

        pdf.ln(5)

    # Recommendations section
    if include_recommendations:
        pdf.add_page()
        recommendations = get_recommendations(results)
        
        pdf.section_title("Personalized Recommendations", "💡")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, "Based on your carbon footprint, here are tailored suggestions to reduce your impact:", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        
        current_category = ""
        for i, rec in enumerate(recommendations, 1):
            if rec["category"] != current_category:
                current_category = rec["category"]
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(39, 174, 96)
                pdf.cell(0, 8, f"\n{current_category}:", new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(0, 0, 0)
            
            priority_colors = {
                "High": (192, 57, 43),
                "Medium": (243, 156, 18),
                "Low": (39, 174, 96),
            }
            color = priority_colors.get(rec["priority"], (0, 0, 0))
            
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*color)
            pdf.cell(15, 7, f"[{rec['priority']}]")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 7, rec["tip"], new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(10)

        # Annual reduction targets
        pdf.section_title("Reduction Targets", "🎯")
        pdf.set_font("Helvetica", "", 10)
        
        target_2030 = COMPARISON_BENCHMARKS["target_2030"]
        if total > target_2030:
            reduction_needed = total - target_2030
            reduction_pct = (reduction_needed / total) * 100
            pdf.cell(0, 8, f"To meet the 2030 Paris Agreement target ({target_2030:,} kg CO2e):", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(192, 57, 43)
            pdf.cell(0, 10, f"  Reduce by {reduction_needed:,.2f} kg CO2e ({reduction_pct:.1f}%)", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_text_color(39, 174, 96)
            pdf.cell(0, 8, "Congratulations! You're already meeting the 2030 Paris Agreement target!", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
        
        pdf.ln(8)

    # Data sources
    pdf.section_title("Data Sources & Methodology", "📚")
    pdf.set_font("Helvetica", "", 9)
    sources = [
        "EPA - US Environmental Protection Agency (Emission Factors Hub)",
        "DEFRA - UK Department for Environment, Food & Rural Affairs",
        "IPCC - Intergovernmental Panel on Climate Change (AR6)",
        "IEA - International Energy Agency (World Energy Outlook)",
        "Our World in Data - CO2 and Greenhouse Gas Emissions",
        "Global Carbon Project - Annual Global Carbon Budget",
    ]
    for source in sources:
        pdf.cell(0, 6, f"  • {source}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5, "Note: Emission factors are estimates based on averages and may vary by region, "
                         "technology, and specific conditions. This report provides a general indication "
                         "of your carbon footprint and should be used for awareness and planning purposes.")
    pdf.set_text_color(0, 0, 0)

    pdf.output(filename)
    return filename


def print_summary(results: dict) -> None:
    """Print a text summary of the carbon footprint results.
    
    Args:
        results: Carbon footprint calculation results
    """
    total = results["total"]
    
    print("\n" + "=" * 60)
    print("CARBON FOOTPRINT SUMMARY")
    print("=" * 60)
    print(f"\nTotal Annual Emissions: {total:,.2f} kg CO2e")
    print(f"Equivalent to: {total/1000:,.2f} tonnes CO2e\n")
    
    print("Breakdown by Category:")
    print("-" * 40)
    categories = [
        ("Transportation", results["transport"]),
        ("Energy", results["energy"]),
        ("Food", results["food"]),
        ("Waste", results["waste"]),
        ("Water", results["water"]),
    ]
    
    for name, value in categories:
        pct = (value / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
        print(f"{name:<15} {value:>10,.2f} kg  ({pct:>5.1f}%) {bar}")
    
    print("-" * 40)
    print(f"{'TOTAL':<15} {total:>10,.2f} kg  (100.0%)")
    print("=" * 60)
    
    # Quick comparison
    comparisons = get_comparison(total)
    global_comp = comparisons["global_average"]
    if global_comp["status"] == "above":
        print(f"\n⚠️  You are {global_comp['difference_pct']:.1f}% ABOVE the global average")
    else:
        print(f"\n✅ You are {global_comp['difference_pct']:.1f}% BELOW the global average")
    
    target_comp = comparisons["target_2030"]
    if target_comp["status"] == "above":
        print(f"🎯 To meet 2030 targets, reduce by {target_comp['difference_pct']:.1f}%")
    else:
        print(f"🎉 You're already meeting 2030 climate targets!")
    print()


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

    # Print text summary
    print_summary(example_results)

    # Generate PDF report
    report_file = generate_pdf_report(
        example_results,
        filename="carbon_report.pdf",
        user_name="John Doe"
    )
    print(f"Carbon footprint report generated: {report_file}")
    print(f"Total emissions: {example_results['total']:,.2f} kg CO2e")
