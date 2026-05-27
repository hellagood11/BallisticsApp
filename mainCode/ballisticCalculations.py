from pyscript import document, when
import csv
import matplotlib.pyplot as plt
import pyscript
class Cartridge:
    def __init__(self, grains, velocity):
        self.grains = grains
        self.velocity = velocity 
        
        # Conversions
        kilograms = grains / 15432.3584                    # 1 kg ≈ 15432.36 grains
        metersPerSec = velocity * 0.3048                 # 1 foot = 0.3048 meters
        
        # Formulas (Metric units)
        self.kineticEnergyJoules = 0.5 * kilograms * (metersPerSec ** 2)
        self.momentumKg_ms = kilograms * metersPerSec

        # Calculate standard Imperial ballistics metrics
        self.kineticEnergy_Imperial = (grains * (velocity ** 2)) / 450436  # foot-pounds (ft-lbs)
        self.momentum_Imperial = (grains * velocity) / 225218              # pound-seconds (lbs-sec)

def calculate_drop_curve(velocity):
    """Calculates bullet gravity drop in inches for distances up to 300 yards."""
    distances = list(range(0, 305, 10)) # 0 to 300 yards in 10-yard jumps
    drops = []
    
    for x in distances:
        if x == 0:
            drops.append(0.0)
            continue
        # Standard gravity time-of-flight drop formula mapped to inches
        time_of_flight = (x * 3) / velocity
        drop_inches = -16.087 * (time_of_flight ** 2) * 12
        drops.append(drop_inches)
        
    return distances, drops

def generate_trajectory_plot(custom_vel):
    """Generates a matplotlib vector chart and injects it straight into the DOM."""
    # Clear any previous figures to prevent memory leak stacking
    plt.clf()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    
    # 1. Plot the User's Custom Bullet Data
    dist_x, drop_y = calculate_drop_curve(custom_vel)
    ax.plot(dist_x, drop_y, label=f"User Custom Round ({custom_vel} FPS)", color="#007BFF", linewidth=2.5)
    
    # 2. Benchmark Samples: Let's read a fast round and a slow round from your CSV for context
    try:
        with open("ammo.csv", mode="r") as file:
            reader = list(csv.DictReader(file))
            # Safely grab two comparative benchmark references if they exist
            if len(reader) >= 2:
                for idx, row in enumerate([reader[0], reader[-1]]):
                    b_name = row['Cartridge']
                    b_vel = float(row['FPS'])
                    bx, by = calculate_drop_curve(b_vel)
                    colors = ["#dc3545", "#28a745"] # Red and green tracking line styles
                    ax.plot(bx, by, label=f"{b_name} ({int(b_vel)} FPS)", color=colors[idx], linestyle="--")
    except Exception:
        pass # Fallback safety line if CSV fails tracking safely

    # Chart Polish and Styling
    ax.set_title("Comparative Bullet Drop Projections", fontsize=12, fontweight="bold")
    ax.set_xlabel("Distance (Yards)", fontsize=10)
    ax.set_ylabel("Drop (Inches)", fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower left")
    
    # Constrain view frame bounds to show drop behavior cleanly
    ax.set_xlim(0, 300)
    
    # Render figure clean directly back onto your designated layout div
    document.querySelector("#graph-output").innerHTML = ""
    pyscript.display(fig, target="graph-output")

def load_ammo_table():
    """Reads the custom metrics CSV file and builds an HTML table string."""
    try:
        html_table = """
        <table class='data-table'>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Cartridge</th>
                    <th>Type</th>
                    <th>Velocity (FPS)</th>
                    <th>Energy (ft-lbs)</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
        """
        
        with open("CartridgeBallistics.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                html_table += f"""
                <tr>
                    <td><strong>#{row['Ranking']}</strong></td>
                    <td>{row['Cartridge']}</td>
                    <td>{row['Type'].capitalize()}</td>
                    <td>{row['FPS']}</td>
                    <td>{row['Energy']}</td>
                    <td>{float(row['Score']):.3f}</td>
                </tr>
                """
        
        html_table += "</tbody></table>"
        document.querySelector("#table-output").innerHTML = html_table
    except Exception as e:
        document.querySelector("#table-output").innerText = f"Error loading CSV: {str(e)}"

@when("click", "#calc-btn")
def calculate(event):
    # Grab inputs safely
    grains_input = document.querySelector("#grains").value
    velocity_input = document.querySelector("#velocity").value

    if not grains_input or not velocity_input:
        return

    try:
        grains = float(grains_input)
        velocity = float(velocity_input)
        
        # Instantiate your Cartridge class
        round_data = Cartridge(grains, velocity)
        
        # Display Imperial results
        document.querySelector("#energy-imp").innerText = f"{round_data.kineticEnergy_Imperial:.2f}"
        document.querySelector("#momentum-imp").innerText = f"{round_data.momentum_Imperial:.4f}"
        
        # Display Metric results
        document.querySelector("#energy-metric").innerText = f"{round_data.kineticEnergyJoules:.2f}"
        document.querySelector("#momentum-metric").innerText = f"{round_data.momentumKg_ms:.4f}"

        # TRIGGER THE DYNAMIC GRAPH RENDERING
        generate_trajectory_plot(velocity)
        
    except ValueError:
        pass

load_ammo_table()