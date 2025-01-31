from base.config import send_data_queue, receive_data_queue
from struct_command import *

MY_ADDR = 0x05
INPUT_ADDR = 0x01
DISCRIMINATION_ADDR = 0x02
RETURN_ADDR = 0x03
ALIGNMENT_ADDR = 0x04
MASTER_ADDR = 0x06 

SHUTTER_SOLENOID_IN_INPUT_ID = 0x01
SOLENOID_A_IN_DISCRIMINATION_ID = 0x01
SOLENOID_B_IN_DISCRIMINATION_ID = 0x02
SOLENOID_C_IN_DISCRIMINATION_ID = 0x03
SOLENOID_ETC_IN_DISCRIMINATION_ID = 0x04
SOLENOID_RETURN_IN_DISCRIMINATION_ID = 0x05
SOLENOID_A_IN_ALIGNMENT_ID = 0x01
SOLENOID_B_IN_ALIGNMENT_ID = 0x02
SOLENOID_C_IN_ALIGNMENT_ID = 0x03

DATA_ON = 0x01
DATA_OFF = 0x02
DATA_STEP = 0x03

class SendDataBaseClass:
    def __init__(self):
        pass
    def make_address(self, myaddress,sendaddress):
        address_send = (myaddress << 4) | sendaddress
        return address_send
    def make_send_data(self, address_send,command,data1=0,data2=0,data3=0):
        send_data = bytearray([address_send,command,data1,data2,data3])
        return send_data
    
class SendConfigurationChange(SendDataBaseClass):
    def __init__(self):
         super().__init__()
    def change_input_configuration(self, rising_speed: int, descending_speed: int):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,CONFIGURATIONCHANGE,rising_speed, descending_speed)
        send_data_queue.put(data_to_send)
    def change_discrimination_configuration(self, setting_speed: int):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,CONFIGURATIONCHANGE,0x00, setting_speed)
        send_data_queue.put(data_to_send)

class SendModuleOperation(SendDataBaseClass):
    def __init__(self):
        super().__init__()
    def send_input_module_start(self):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_input_module_stop(self):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_discrimination_module_start(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_discrimination_module_stop(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_return_module_start(self):
        address_send = self.make_address(MY_ADDR,RETURN_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_return_module_stop(self):
        address_send = self.make_address(MY_ADDR,RETURN_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_alignment_module_start(self):
        address_send = self.make_address(MY_ADDR,ALIGNMENT_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_alignment_module_stop(self):
        address_send = self.make_address(MY_ADDR,ALIGNMENT_ADDR)
        data_to_send = self.make_send_data(address_send,MODULEOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_all_module_stop(self):
        self.send_input_module_stop()
        self.send_discrimination_module_stop()
        self.send_return_module_stop()
        self.send_all_module_stop()

class SendMotorReset(SendDataBaseClass):
    def __init__(self):
        super().__init__()
    def discrimination_motor_reset(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORRESET)
        send_data_queue.put(data_to_send)
    def return_motor_reset(self):
        address_send = self.make_address(MY_ADDR,RETURN_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORRESET)
        send_data_queue.put(data_to_send)

class SendMotorManualOperation(SendDataBaseClass):
    def __init__(self):
        super().__init__()
    def send_input_manual_start(self):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_input_manual_stop(self):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_discrimination_manual_start(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_discrimination_manual_stop(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)
    def send_discrimination_manual_step(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_STEP)
        send_data_queue.put(data_to_send)
    def send_return_manual_start(self):
        address_send = self.make_address(MY_ADDR,RETURN_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_ON)
        send_data_queue.put(data_to_send)
    def send_return_manual_stop(self):
        address_send = self.make_address(MY_ADDR,RETURN_ADDR)
        data_to_send = self.make_send_data(address_send,MOTORMANUALOPERATION,DATA_OFF)
        send_data_queue.put(data_to_send)

class SendSolenoidIndividualOperation(SendDataBaseClass):
    def __init__(self):
        super().__init__()
    def operate_shutter_solenoid_in_input(self):
        address_send = self.make_address(MY_ADDR,INPUT_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SHUTTER_SOLENOID_IN_INPUT_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_a_in_discrimination(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_A_IN_DISCRIMINATION_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_b_in_discrimination(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_B_IN_DISCRIMINATION_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_c_in_discrimination(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_C_IN_DISCRIMINATION_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_etc_in_discrimination(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_ETC_IN_DISCRIMINATION_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_return_in_discrimination(self):
        address_send = self.make_address(MY_ADDR,DISCRIMINATION_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_RETURN_IN_DISCRIMINATION_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_a_in_alignment(self):
        address_send = self.make_address(MY_ADDR,ALIGNMENT_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_A_IN_ALIGNMENT_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_b_in_alignment(self):
        address_send = self.make_address(MY_ADDR,ALIGNMENT_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_B_IN_ALIGNMENT_ID)
        send_data_queue.put(data_to_send)
    def operate_solenoid_c_in_alignment(self):
        address_send = self.make_address(MY_ADDR,ALIGNMENT_ADDR)
        data_to_send = self.make_send_data(address_send,SOLENOIDINDIVIDUALOPERATION,SOLENOID_C_IN_ALIGNMENT_ID)
        send_data_queue.put(data_to_send)