from Message import Message

from Mapping import Mapping

from Modulator import Modulator

from Transmitter import Transmitter

from Channel import Channel

from Receiver import Receiver

from MeritFunctions import MeritFunctions

from SimulationSync import SimulationSync

import Global

from beeprint import pp
# import beeprint as pp

from matplotlib import pyplot as plt

import generalLibrary as lib

class Main(object):
    def __init__(self, DEBUG=False, PLOT=False):
        """Constructor"""
        self.DEBUG = DEBUG
        
        self.PLOT = PLOT
        
        if self.DEBUG:
            print('Running Main...')
            pass
        
        ###########################################################################
        # >>>>>>>>>> CREATE SIMULATION SYNC OBJECT
        
        # Create object for SimulationSync, used for overral simulation control and debug.
        self.sync_obj = SimulationSync(
            DEBUG = self.DEBUG,
            previous = "Main"
            )
        
        ###########################################################################
        # >>>>>>>>>> CREATE MESSAGE OBJECT
        
        # Creates message object.
        self.message_obj = Message(
            input_info=Global.input_info,
            n_frames=len(Global.input_info["data"]),
            sync_obj = self.sync_obj
        )
        
        if self.DEBUG:
            print(self.message_obj.getInputInfo())
            pass
        
        # Set previous for debug
        self.sync_obj.setPrevious("Main")
        
        ###########################################################################
        # >>>>>>>>>> CONVERT MESSAGES TO LIST OF BITSTREAMS
            
        # Converts it from its original type to a stream of bits (stored in bitstream_frames)
        self.message_obj.convertsToBitstream()
        
        ###########################################################################
        # >>>>>>>>>> FOR EACH MESSAGE, ITERATE THROUGH ITS BITSTREAM FROM TRANSMITTER UP TO RECEIVER
        
        # For loop for each frame bitstream (each information to be sent in Global.input_info)
        for curr_frame in self.message_obj.getBitstreamFrames():
            if self.DEBUG:
                print(f'curr_frame = {curr_frame}')
                pass
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> FOR THAT BITSTREAM, STARTS MODULATION, GIVEN MODULATION CONFIG
            
            # Modulator object.
            self.modulator_obj = Modulator(
                bitstream_frame=curr_frame,
                modulation_config=Global.modulation_config[Global.modulation_index],
                mapping_config=Global.mapping_config[Global.mapping_index],
                sync_obj = self.sync_obj
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> CREATES MODULATION OBJECT, DEPENDING ON THE TYPE (EX: OFDM)
            
            # Creates the modulator object, depending on the 'modulation_type' in 'modulation_config'
            self.modulator_obj.createModulator()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> APPLY MODULATION GIVEN CHOOSEN TYPE (EX: OFDM)
            
            # Applies the modulation, with modulation object just created
            self.modulator_obj.applyModulation()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> GET THE LIST OF DATA TO BE TRANSMITTED, AFTER MODULATION
            # >>>>>>>>>> DEPENDING ON TRANSMITTER THROUGHPUT, MORE THAN ONE TX_DATA
            # >>>>>>>>>> IS NEEDED
            
            # Return a list of symbols to be transmitted.
            # This list is defined by the throughput of the modulator
            self.tx_data_list = self.modulator_obj.getTxDataList()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> STARTS TRANSMITTER, GIVEN CONFIG
            
            # Transmitter object.
            self.transmitter_obj = Transmitter(
                transmitter_config = Global.transmitter_config,
                tx_data_list = self.tx_data_list,
                sync_obj = self.sync_obj
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> APPLY DAC ON TX_DATA, CONVERTING TO ANALOG. CAN BE 
            # >>>>>>>>>> BYPASSED BY Global.bypass_dict["DAC"]
            
            # Applies DAC
            self.transmitter_obj.applyDAC()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES OPTICAL POWER, DEPENDING ON THE LIGHTSOURCES
            # >>>>>>>>>> OR CAN BE BYPASSED BY Global.bypass_dict["LightSource"]
            
            # Calculates the optical power provided by the light sources
            self.transmitter_obj.calculatesOpticalPower()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> RETRIEVE TX_DATA LIST FOR THE CHANNEL
            
            # Gets the list of optical powers to be transmitted
            tx_data_list = self.transmitter_obj.getTxOpticalOutList()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            if self.PLOT:
                handle = plt.figure(figsize=(8,2))
                lib.plotTxRxDataList(tx_data_list, 'TX DATA', handle, self.sync_obj, show = False)
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            
            ###########################################################################
            # >>>>>>>>>> CREATES CHANNEL GIVEN INPUT TX_DATA LIST
            
            # Channel object
            self.channel_obj = Channel(
                tx_data_in = tx_data_list,
                sync_obj = self.sync_obj
            )
            
            # If not bypassing Channel, calculates the channel impulse response (CIR)
            if not Global.bypass_dict["Channel"]:
                
                ###########################################################################
                # >>>>>>>>>> CALCULATES CHANNEL RESPONSE FOR EACH LIGHTSOURCE, IF NOT BYPASSED
                
                raise ValueError(f"\n\n***Error --> Calculation of channel response for each LightSource, when NOT bypassing 'Channel', not implemented yet!\n")
            
                # claculates the impulse response
                self.channel_obj.calculatesChannelResponse()
                
            else:
                
                ###########################################################################
                # >>>>>>>>>> IF BYPASSING (Global.bypass_dict["Channel"]) MUST SET THE 
                # >>>>>>>>>> CIR FOR EACH LIGHTSOURCE
                
                # sets the channel response for each lamp
                # If lightsource is not bypassed
                if not Global.bypass_dict["LightSource"]:
                    # setChannelResponse for each lamp
                    raise ValueError(f"\n\n***Error --> Set channel response for each LightSource, when bypassing 'Channel', not implemented yet!\n")
                    # self.channel_obj.setChannelResponse([...])
                    
                else:
                    # Set single channel response (list of 1 position)
                    self.channel_obj.setChannelResponse(Global.list_of_channel_response)
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> APPLY EACH CIR (FOR EACH LIGHTSOURCE) TO EACH TX_DATA.
            
            # After channel reponse set, apply it to each lamp.
            self.channel_obj.applyChannelResponse()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> GET RX_DATA LIST CONVOLVED BY CHANNEL AFTER ADDING NOISE.
            
            # Gets the list of optical powers at the receiver, after convolution on channel response, and noise addition.
            rx_data_list = self.channel_obj.getRxDataOut()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            if self.PLOT:
                lib.plotTxRxDataList(rx_data_list, 'RX DATA', handle, self.sync_obj, show = True)
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> STARTS RECEIVER, GIVEN CONFIG
            
            # Receiver object.
            self.receiver_obj = Receiver(
                receiver_config = Global.receiver_config,
                roic_config = Global.roic_config,
                rx_data_list = rx_data_list,
                sync_obj = self.sync_obj
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES PHOTOCURRENTS, DEPENDING ON THE DETECTORS
            
            # Calculates the photocurrents, provided by the detectors
            self.receiver_obj.calculatesPhotocurrent()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES THE OUTPUT VOLTAGE
            
            # Calculates the output voltage
            self.receiver_obj.calculatesOutVoltage()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> APPLY ADC ON RX_DATA, CONVERTING FROM ANALOG TO DIGITAL
            
            # Applies ADC
            self.receiver_obj.applyADC()
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            ###########################################################################
            # >>>>>>>>>> GET ADC RX_DATA TO PASS FOR DE-MODULATOR
            
            self.modulator_obj.setRxDataList
            (
                self.receiver_obj.getAdcRxDataList()
            )
            
            # Set previous for debug
            self.sync_obj.setPrevious("Main")
            
            
            pp(self.receiver_obj)
        
        
        # # Merit Funcions object
        # self.merit_functions_obj = MeritFunctions()
        
        # Set previous for debug
        self.sync_obj.setPrevious("Main")
            
        # Get recovered info from the received stream of bits, and converts back to original form.
        recovered_info = self.message_obj.BitstreamToMessage(rx_bitstream_frames = self.message_obj.getBitstreamFrames())
        
        if DEBUG:
            print(f'recovered_info = {recovered_info}')
            # print(f'type = {type(info[0])}')
            pass
        
        # Prints full simulation path
        print(self.sync_obj.getSimulationPath())
        
        pass

    def getMessageObj(self):
        """Returns value of self.message_obj"""
        
        return self.message_obj

    def setMessageObj(self, message_obj):
        """Set new value for self.message_obj"""
        
        self.message_obj = message_obj

    def getMappingObj(self):
        """Returns value of self.mapping_obj"""
        
        return self.mapping_obj

    def setMappingObj(self, mapping_obj):
        """Set new value for self.mapping_obj"""
        
        self.mapping_obj = mapping_obj

    def getModulatorObj(self):
        """Returns value of self.modulator_obj"""
        
        return self.modulator_obj

    def setModulatorObj(self, modulator_obj):
        """Set new value for self.modulator_obj"""
        
        self.modulator_obj = modulator_obj

    def getTransmitterObj(self):
        """Returns value of self.transmitter_obj"""
        
        return self.transmitter_obj

    def setTransmitterObj(self, transmitter_obj):
        """Set new value for self.transmitter_obj"""
        
        self.transmitter_obj = transmitter_obj

    def getChannelObj(self):
        """Returns value of self.channel_obj"""
        
        return self.channel_obj

    def setChannelObj(self, channel_obj):
        """Set new value for self.channel_obj"""
        
        self.channel_obj = channel_obj

    def getReceiverObj(self):
        """Returns value of self.receiver_obj"""
        
        return self.receiver_obj

    def setReceiverObj(self, receiver_obj):
        """Set new value for self.receiver_obj"""
        
        self.receiver_obj = receiver_obj

    def getMeritFunctionsObj(self):
        """Returns value of self.merit_functions_obj"""
        
        return self.merit_functions_obj

    def setMeritFunctionsObj(self, merit_functions_obj):
        """Set new value for self.merit_functions_obj"""
        
        self.merit_functions_obj = merit_functions_obj
    
    
if __name__ == "__main__":
    
    print("Starting VLC Simulator...")
    
    
    main_obj = Main(DEBUG=True, PLOT=True)
    # main_obj = Main(DEBUG=False, PLOT=True)
    
