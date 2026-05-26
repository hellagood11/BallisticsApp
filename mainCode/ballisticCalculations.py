class cartridge:
    def __init__(self, grains, velocity):
        self.grains = grains
        self.velocity = velocity 
        kilograms = grains / 15432.09876543
        metersPerSec = velocity / 0.3048
        kineticEnergy = 0.5 * kilograms * metersPerSec
        momentum = kilograms * metersPerSec



