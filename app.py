def calculate_ideal_settings(weight, age, sex, ph, pao2, paco2, bicarb, base_excess, cao2):
    """
    Calculate ideal ventilator settings and the most appropriate mode.
    """
    print("\n=== Ideal Ventilator Settings ===")

    # Define age-based respiratory rate ranges
    age_rate_ranges = {
        "Infant (birth–1 year)": (30, 60),
        "Toddler (1–3 years)": (24, 40),
        "Preschooler (3–6 years)": (22, 34),
        "School-age (6–12 years)": (18, 30),
        "Adolescent (12–18 years)": (12, 16),
    }

    # Determine age group and respiratory rate range
    if age <= 1:
        age_group = "Infant (birth–1 year)"
    elif age <= 3:
        age_group = "Toddler (1–3 years)"
    elif age <= 6:
        age_group = "Preschooler (3–6 years)"
    elif age <= 12:
        age_group = "School-age (6–12 years)"
    else:
        age_group = "Adolescent (12–18 years)"

    min_rate, max_rate = age_rate_ranges[age_group]

    # FiO2 adjustment
    if pao2 < 50:
        fio2 = 0.6  # Increase FiO2
    elif pao2 > 80:
        fio2 = 0.3  # Decrease FiO2
    else:
        fio2 = 0.4  # Normal FiO2 range

    # PEEP adjustment
    if base_excess < -2 or ph < 7.35:
        peep = 6  # Increase PEEP for acidosis
    else:
        peep = 4  # Normal PEEP for stable patients

    # PIP and Pressure Support calculations
    pip = 15 + weight  # Approximate PIP based on weight
    pressure_support = 10 if ph < 7.35 else 8  # Adjust for acidosis or stable conditions

    # Respiratory rate adjustment based on PaCO2
    if paco2 > 45:  # Hypercapnia
        respiratory_rate = max(min_rate, max_rate)  # Increase RR within the range
    elif paco2 < 35:  # Hypocapnia
        respiratory_rate = min(min_rate, max_rate)  # Decrease RR within the range
    else:
        respiratory_rate = (min_rate + max_rate) // 2  # Use the mid-point of the range

    # iTime
    itime = 0.4 if age <= 1 else 0.6  # Shorter iTime for neonates

    # Mode selection
    if paco2 > 45:  # Hypercapnia, controlled ventilation
        mode = "PCSIMVPS"
    elif ph < 7.35:  # Acidosis
        mode = "ACPC"
    elif ph >= 7.35 and 35 <= paco2 <= 45:  # Stable patient
        mode = "PS"
    else:
        mode = "CPAP"

    # Recommended settings
    settings = {
        "Respiratory Rate": respiratory_rate if mode in ["PCSIMVPS", "ACPC"] else "N/A (Spontaneous)",
        "PIP": pip if mode in ["PCSIMVPS", "ACPC"] else "N/A",
        "PEEP": peep,
        "Pressure Support": pressure_support if mode == "PS" else "N/A",
        "iTime": itime if mode in ["PCSIMVPS", "ACPC"] else "N/A",
        "FiO2": fio2
    }

    # Display recommendations
    print(f"\nRecommended Mode: {mode}")
    print(f"Age Group: {age_group}")
    for key, value in settings.items():
        print(f"  {key}: {value}")

    return mode, settings


def titrate_settings(previous_settings, ph, paco2):
    """
    Adjust settings to normalize blood gas results.
    """
    print("\n=== Titration Recommendations ===")
    adjustments = {}

    # Adjust Respiratory Rate
    if paco2 > 45:  # Hypercapnia
        adjustments["Respiratory Rate"] = previous_settings.get("Respiratory Rate", 20) + 2
    elif paco2 < 35:  # Hypocapnia
        adjustments["Respiratory Rate"] = max(previous_settings.get("Respiratory Rate", 20) - 2, 10)

    # Adjust PEEP for acidosis or alkalosis
    if ph < 7.35:  # Acidosis
        adjustments["PEEP"] = min(previous_settings.get("PEEP", 5) + 1, 10)
    elif ph > 7.45:  # Alkalosis
        adjustments["PEEP"] = max(previous_settings.get("PEEP", 5) - 1, 3)

    # Display adjustments
    for key, value in adjustments.items():
        print(f"  {key}: {value}")
    return adjustments


def main():
    print("=== Pediatric and Neonatal Ventilator Settings Calculator ===")
    # Input patient data
    weight = float(input("Enter patient weight (kg): "))
    age = float(input("Enter patient age (years): "))
    sex = input("Enter patient sex (M/F): ").upper()
    
    # Input blood gas results
    print("\nEnter most recent blood gas results:")
    ph = float(input("  pH: "))
    pao2 = float(input("  PaO2 (mmHg): "))
    paco2 = float(input("  PaCO2 (mmHg): "))
    bicarb = float(input("  Bicarb (mEq/L): "))
    base_excess = float(input("  Base Excess (mEq/L): "))
    cao2 = float(input("  CaO2 (mL O2/dL): "))

    # Calculate ideal settings
    mode, ideal_settings = calculate_ideal_settings(weight, age, sex, ph, pao2, paco2, bicarb, base_excess, cao2)

    # Input previous settings for titration
    print("\nEnter previous ventilator settings for titration (optional):")
    previous_settings = {
        "Respiratory Rate": float(input("  Previous Rate (breaths/min): ") or 20),
        "PEEP": float(input("  Previous PEEP (cm H2O): ") or 5)
    }

    # Titrate settings
    titrate_settings(previous_settings, ph, paco2)


if __name__ == "__main__":
    main()
