from pyscript import document, when

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
        
    except ValueError:
        pass