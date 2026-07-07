import pandas as pd
from py_ballisticcalc import *
from pyscript import document, when
import matplotlib.pyplot as plt
from io import StringIO

@when("click", "#wind-calc-btn")
def calculate_trajectory(event):

    #getting user inputs from the HTML form into python variables
    bc = float(document.querySelector("#bc").value)
    velocity = float(document.querySelector("#velocity").value)
    sightHeight = float(document.querySelector("#sightHeight").value)
    windSpeed = float(document.querySelector("#windSpeed").value)
    windDirection = float(document.querySelector("#windDir").value)
    maxRange = float(document.querySelector("#maxRange").value)
    rangeStep = float(document.querySelector("#rangeStep").value)
    tableSelection = document.querySelector("#ballisticTableSelection").value
    match tableSelection:
        case "TableG1":
            tableSelection = TableG1
        case "TableG7":
            tableSelection = TableG7
        case "TableG2":
            tableSelection = TableG2
        case "TableG5":
            tableSelection = TableG5
        case "TableG6":
            tableSelection = TableG6
        case "TableG8":
            tableSelection = TableG8
        case "TableGI":
            tableSelection = TableGI
        case "TableGS":
            tableSelection = TableGS
        case "TableRA4":
            tableSelection = TableRA4

    #calculating the zero elevation
    zero = Shot(weapon=Weapon(sight_height=sightHeight), ammo=Ammo(DragModel(bc, tableSelection), mv=Velocity.FPS(velocity)))
    calc = Calculator()
    #setting the zero distance to 100 yards for the calculation
    zero_distance = Distance.Yard(100)  # Assuming zero at 100 yards
    zero_elevation = calc.set_weapon_zero(zero, zero_distance)
    
    # formatting the zero elevation output to display in the HTML
    adj_str = str(zero_elevation << PreferredUnits.adjustment)
    document.querySelector("#zeroOutput").innerText = f"Zero Elevation (100 yards): {adj_str} MOA"

    # calculating the trajectory and generating the range card data
    zero.winds = [Wind(Velocity.MPH(windSpeed), Angular.OClock(windDirection))]
    range_card = calc.fire(zero, trajectory_range=maxRange, trajectory_step=rangeStep)
    df = range_card.dataframe(True)[['distance', 'velocity', 'mach', 'time', 'height', 'drop_angle', 'windage', 'windage_angle']]

    # rounding the values in the dataframe to a specified number of decimal places for better readability
    df = df.round({'distance': 0, 'velocity': 0, 'mach': 3, 'time': 3, 'height': 2, 'drop_angle': 2, 'windage': 2, 'windage_angle': 2})

    # renaming the columns of the dataframe to more user-friendly names for display in the HTML table
    df.columns = ['Distance (yd)', 'Velocity (fps)', 'Mach', 'Time (s)', 'Height (in)', 'Drop Angle (°)', 'Windage (in)', 'Windage Angle (°)']

    # converting the dataframe to an HTML table and inserting it into the designated output div in the HTML
    html_table = df.to_html(index=False, classes='data-table', border=0, justify='center', escape=False)
    document.querySelector("#windageElevationTableOutput").innerHTML = html_table

    # Create the stacked subplots sharing an x-axis with standard clean backgrounds
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, constrained_layout=True)

    # Top Subplot: Real-world Drop Profile
    ax1.plot(df["Distance (yd)"], df["Height (in)"], color="#1f77b4", marker="o", linewidth=2.5, markersize=4, label="Bullet Path")
    ax1.axhline(0, color="#7f7f7f", linestyle="--", linewidth=1, label="Line of Sight (Zero)") # Zero reference line
    ax1.set_title("Vertical Trajectory (Drop Profile)", fontsize=11, fontweight="bold", loc="left")
    ax1.set_ylabel("Drop / Height (in)")
    ax1.grid(True, alpha=0.5, linestyle="--")
    ax1.legend(loc="lower left")
    
    # CRITICAL: Invert the y-axis so gravity visually pulls the path down
    ax1.invert_yaxis()

    # Bottom Subplot: Wind Drift Profile
    ax2.plot(df["Distance (yd)"], df["Windage (in)"], color="#ff7f0e", marker="o", linewidth=2.5, markersize=4, label="Wind Drift")
    ax2.axhline(0, color="#7f7f7f", linestyle="--", linewidth=1) # Centerline reference
    ax2.set_title("Horizontal Deflection (Windage Drift)", fontsize=11, fontweight="bold", loc="left")
    ax2.set_xlabel("Distance (Yards)")
    ax2.set_ylabel("Windage Drift (in)")
    ax2.grid(True, alpha=0.5, linestyle="--")
    ax2.legend(loc="upper left")

    # Save to SVG buffer to match your layout implementation flawlessly
    svg_buffer = StringIO()
    fig.savefig(svg_buffer, format="svg", bbox_inches="tight")
    plt.close(fig)

    # Inject the responsive vector graphic straight into your dashboard placeholder
    document.querySelector("#windageElevationGraphOutput").innerHTML = svg_buffer.getvalue()