import pandas as pd
from py_ballisticcalc import *
from pyscript import document, when

@when("click", "#wind-calc-btn")
def calculate_trajectory(event):
    bc = float(document.querySelector("#bc").value)
    velocity = float(document.querySelector("#velocity").value)
    sightHeight = float(document.querySelector("#sightHeight").value)
    windSpeed = float(document.querySelector("#windSpeed").value)
    windDirection = float(document.querySelector("#windDir").value)
    maxRange = float(document.querySelector("#maxRange").value)
    rangeStep = float(document.querySelector("#rangeStep").value)

    zero = Shot(weapon=Weapon(sight_height=sightHeight), ammo=Ammo(DragModel(bc, TableG7), mv=Velocity.FPS(velocity)))
    calc = Calculator()

    zero_distance = Distance.Yard(100)  # Assuming zero at 100 yards
    zero_elevation = calc.set_weapon_zero(zero, zero_distance)
    
    adj_str = str(zero_elevation << PreferredUnits.adjustment)
    document.querySelector("#zeroOutput").innerText = f"Zero Elevation (100 yards): {adj_str} MOA"

    zero.winds = [Wind(Velocity.MPH(windSpeed), Angular.OClock(windDirection))]
    range_card = calc.fire(zero, trajectory_range=maxRange, trajectory_step=rangeStep)
    df = range_card.dataframe(True)[['distance', 'velocity', 'mach', 'time', 'height', 'drop_angle', 'windage', 'windage_angle']]

    df = df.round({'distance': 0, 'velocity': 0, 'mach': 3, 'time': 3, 'height': 2, 'drop_angle': 2, 'windage': 2, 'windage_angle': 2})

    df.columns = ['Distance (yd)', 'Velocity (fps)', 'Mach', 'Time (s)', 'Height (in)', 'Drop Angle (°)', 'Windage (in)', 'Windage Angle (°)']

    html_table = df.to_html(index=False, classes='data-table', border=0, justify='center', escape=False)
    document.querySelector("#windageElevationTableOutput").innerHTML = html_table

