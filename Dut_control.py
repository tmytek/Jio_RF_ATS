import subprocess
from logHandler import LogHandler

class Jio_ftdi:
    def __init__(self):
        LogHandler.log("Jio_ftdi initialized")

    def channel_setting(self, chain, IC_no, Channel, mode, polarity, diable, com_gain, ele_gain, phase):
        #cmd_str = "--channel 1 1 1 0 0 0 0 0 0"
        try:
            result = subprocess.run(
            ['python', './Jio_ftdi_control/jio_bfic_controller.py', '--channel', f"{chain}", f"{IC_no}", f"{Channel}", f"{mode}", f"{polarity}", f"{diable}", f"{com_gain}", f"{ele_gain}", f"{phase}"],
            capture_output=True,
            text=True
            )
            LogHandler.log(f"標準輸出： {result.stdout}")
            LogHandler.log(f"標準錯誤： {result.stderr}")
            LogHandler.log(f"回傳碼： {result.returncode}")
        except Exception as e:
            LogHandler.log(f"Error BFIC channel_setting")
        
    def channel_disable_all(self):
        try:
            result = subprocess.run(
            ['python', './Jio_ftdi_control/jio_bfic_controller.py', '--dis', f"1"],
            capture_output=True,
            text=True
            )
            LogHandler.log(f"標準輸出： {result.stdout}")
            LogHandler.log(f"標準錯誤： {result.stderr}")
            LogHandler.log(f"回傳碼： {result.returncode}")
        except Exception as e:
            LogHandler.log(f"Error for BFIC diable all")
        
    
    def ud_att_tx(self, ud_att):
        try:
            result = subprocess.run(
            ['python', './Jio_ftdi_control/jio_udic_controller.py', '--att_tx', f"{ud_att}"],
            capture_output=True,
            text=True
            )
            LogHandler.log(f"標準輸出： {result.stdout}")
            LogHandler.log(f"標準錯誤： {result.stderr}")
            LogHandler.log(f"回傳碼： {result.returncode}")
        except Exception as e:
            LogHandler.log(f"Error UDIC attenuator Tx setting")
    
    def ud_att_rx(self, ud_att):
        try:
            result = subprocess.run(
            ['python', './Jio_ftdi_control/jio_udic_controller.py', '--att_rx', f"{ud_att}"],
            capture_output=True,
            text=True
            )
            LogHandler.log(f"標準輸出： {result.stdout}")
            LogHandler.log(f"標準錯誤： {result.stderr}")
            LogHandler.log(f"回傳碼： {result.returncode}")
        except Exception as e:
            LogHandler.log(f"Error UDIC attenuator Tx setting")

    def bfic_att(self, pol=1, com=0, ele=0):
        try:
            result = subprocess.run(
            ['python', './Jio_ftdi_control/jio_bfic_controller.py', '--pol', f"{pol}", '--com', f"{com}", '--ele', f"{ele}"],
            capture_output=True,
            text=True
            )
            LogHandler.log(f"標準輸出： {result.stdout}")
            LogHandler.log(f"標準錯誤： {result.stderr}")
            LogHandler.log(f"回傳碼： {result.returncode}")
        except Exception as e:
            LogHandler.log(f"Error UDIC attenuator Tx setting")