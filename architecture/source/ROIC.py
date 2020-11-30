import Global

from Virtuoso import Virtuoso

from Tanner import Tanner

class ROIC(object):
    def __init__(self, circuit_type, waves_name, sync_obj):
        """Constructor of LightSource. Receives the light_type"""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("ROIC") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("ROIC")
        
        if self.DEBUG:
            print('Running ROIC...')
        
        # Stores the circuit topology. Ex: APS, Bouncing Pixel, etc.
        self.circuit_type = circuit_type
        
        # Stores the list of wave names to be delivered
        self.waves_name = waves_name

        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = Global.circuit_simulation

        # Curve that translates how to convert from photocurrent to voltage.
        self.linearity_curve = {"photocurrent": [], "voltage": []}

        # Defines the simulator to be used, if appliable.
        self.which_simulator = Global.which_simulator

        # Stores the netlist of the circuit.
        self.netlist = None

        # Path to netlist of the circuit.
        self.netlist_path = None
        

    def convertsToWaves(self, current_list):
        """Converts a given photocurrent list into associated waves (simulated or not). If flag to use circuit_simulation is active, then calls the Simulator"""
        
        self.sync_obj.appendToSimulationPath("convertsToWaves @ ROIC")
        
        # Set previous for debug
        self.sync_obj.setPrevious("ROIC")
        
        if self.circuit_simulation:
            
            # Calls simulator
            roic_waves_list = self.callSimulator(current_list)
            
            raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at Global.which_simulator = True\n")
        
        else:
            
            raise ValueError(f"\n\n***Error --> ROIC voltage calculations while not bypassed, and circuit_simulation off, is not supported yet.\n")
            
            roic_waves_list = []
            for current in current_list:
                
                voltage = current
                
                roic_waves_list.append(voltage)
                
        return roic_waves_list
        
        
    def callSimulator(self, current_list):
        """Calls the desired circuit simulator, given the 'circuit_type', and arrat of currents to be simulated."""
        
        self.sync_obj.appendToSimulationPath("callSimulator @ ROIC")
        
        # Set previous for debug
        self.sync_obj.setPrevious("ROIC")
        
        raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at Global.which_simulator = True\n")
        
        # Needs to use 'self.circuit_type' an 'self.which_simulator'
        # Uses ssh to call simulator
        
        if self.which_simulator == "Virtuoso":
            
            simulator = Virtuoso(
                netlist = "MY_NETLIST",
                sync_obj = self.sync_obj
            )

        elif self.which_simulator == "Tanner":
            
            simulator = Tanner(
                netlist = "MY_NETLIST",
                sync_obj = self.sync_obj
            )
            
        else:
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > at Global.which_simulator is not supported!\n")
        
        roic_out_list = []
        for current in current_list:
            
            # Set previous for debug
            self.sync_obj.setPrevious("ROIC")
            
            # Setup the simulator
            simulator.setup(currents = current)
            
            # Set previous for debug
            self.sync_obj.setPrevious("ROIC")
            
            # Start the simulator
            simulator.start()
            
            # Set previous for debug
            self.sync_obj.setPrevious("ROIC")
            
            abort = False
            # Keep doing simulation while not aborted
            while not abort:
                
                # abort simulation
                abort = simulator.stop()
            
            # Set previous for debug
            self.sync_obj.setPrevious("ROIC")
            
            waves_list = []
            # Get the desired waves, depending on the circuit
            for wave in self.waves_name:
                # append the waves list of interest
                waves_list.append(simulator.getWave(wave = wave))
            
            # Append list of waves to the roic list output
            roic_out_list.append(waves_list)
        
        return roic_out_list
        
        
    def getCircuitType(self):
        """Returns value of self.circuit_type"""
        
        return self.circuit_type

    def setCircuitType(self, circuit_type):
        """Set new value for self.circuit_type"""
        
        self.circuit_type = circuit_type

    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    def getWhichSimulator(self):
        """Returns value of self.which_simulator"""
        
        return self.which_simulator

    def setWhichSimulator(self, which_simulator):
        """Set new value for self.which_simulator"""
        
        self.which_simulator = which_simulator

    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    def getNetlistPath(self):
        """Returns value of self.netlist_path"""
        
        return self.netlist_path

    def setNetlistPath(self, netlist_path):
        """Set new value for self.netlist_path"""
        
        self.netlist_path = netlist_path
