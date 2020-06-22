from Transmitter import Transmitter

class LightSource(Transmitter):
    def __init__(self, light_type, var1, var2):
        """Constructor of transmitter. Receives the light_type"""

        Transmitter.__init__(self, parent_var1 = var1, parent_var2 = var2)
        

        # Stores the light type. Ex: LED, Laser, etc.
        self.light_type = "LED"

        # Stores the PSD (W/nm) over the wave number (nm)
        self.psd = {"wave_number": [], "psd": []}

        # Stores the intensities (W/m2) emitted by that light source over time (s).
        self.intensity = {"time": [], "intensity": []}

        # Stores the path to the database file, from where we get all data for that light source.
        self.database = r"..\Databases"
    
        pass

    def getIntensityAtDistance(self, distance):
        """Returns the intensity (W) for a given distance (m)."""
        pass
    
