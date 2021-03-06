class Detector(object):
    def __init__(self, light_type, position, angle, DEBUG=False):
        """Constructor of LightSource. Receives the light_type"""
        
        if DEBUG:
            print('Running Detector...')
        
        

        # Stores the detector type. Ex: photodiode, phototransistor, LDR.
        self.detector_type = "photodiode"

        # Stores the PSD (W/nm) over the wave number (nm)
        self.psd = {"wave_number": [], "psd": []}

        # Stores the intensities (W/m2) emitted by that light source over time (s).
        self.intensity = {"time": [], "intensity": []}

        # Stores the path to the database file, from where we get all data for that detector.
        self.database = r"..\Databases"

        # Contains the position for that light source. Used for ray tracing, if appliable.
        self.position = position

        # Contains the angle for that light source. Used for ray tracing, if appliable.
        self.angle = angle

        # Curve that translates how to convert from optical power to photocurrent.
        self.linearity_curve = {"optical_power": [], "photocurrent": []}

        # Info regarding the FOV of such detector.
        self.FOV = None
    
        pass

    def convertsToPhotocurrent(self, power):
        """Converts a given optical power into photocurrent."""
        pass
    

    def loadsJSONData(self):
        """Loads in the JSON data for that detector."""
        pass
    

    def getDetectorType(self):
        """Returns value of self.detector_type"""
        
        return self.detector_type

    def setDetectorType(self, detector_type):
        """Set new value for self.detector_type"""
        
        self.detector_type = detector_type

    def getPsd(self):
        """Returns value of self.psd"""
        
        return self.psd

    def setPsd(self, psd):
        """Set new value for self.psd"""
        
        self.psd = psd

    def getIntensity(self):
        """Returns value of self.intensity"""
        
        return self.intensity

    def setIntensity(self, intensity):
        """Set new value for self.intensity"""
        
        self.intensity = intensity

    def getDatabase(self):
        """Returns value of self.database"""
        
        return self.database

    def setDatabase(self, database):
        """Set new value for self.database"""
        
        self.database = database

    def getPosition(self):
        """Returns value of self.position"""
        
        return self.position

    def setPosition(self, position):
        """Set new value for self.position"""
        
        self.position = position

    def getAngle(self):
        """Returns value of self.angle"""
        
        return self.angle

    def setAngle(self, angle):
        """Set new value for self.angle"""
        
        self.angle = angle

    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    def getFOV(self):
        """Returns value of self.FOV"""
        
        return self.FOV

    def setFOV(self, FOV):
        """Set new value for self.FOV"""
        
        self.FOV = FOV
