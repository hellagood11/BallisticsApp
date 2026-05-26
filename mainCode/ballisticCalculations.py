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
