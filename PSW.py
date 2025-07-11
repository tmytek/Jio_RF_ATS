import pyvisa
import sys
import time
import re
from logHandler import LogHandler

class PSW:
    
    def __init__(self):
        self.rm = None
        self.inst = None

    def INIT(self, resource_str):
        """初始化儀器連線，並設定WLAN EVM單次量測"""
        try:
            rm = pyvisa.ResourceManager()
            # 列出所有可用的資源

            # 連接到 COM3 (請根據實際情況修改)
            #inst = rm.open_resource('ASRL3::INSTR')
            self.inst = rm.open_resource(resource_str)
            # 設定通訊參數
            self.inst.baud_rate = 9600
            self.inst.data_bits = 8
            self.inst.parity = pyvisa.constants.Parity.none
            self.inst.stop_bits = pyvisa.constants.StopBits.one
            self.inst.timeout = 5000  # ms

            # 寫入資料
            #self.inst.write('COMMAND\r\n')

            # 讀取資料
            #response = self.inst.read()
            #print(response)

            return True
        except Exception as e:
            LogHandler.log(f"[INIT] Error: {e}")
            self.close()
            return False
    
    def close(self):
        """關閉儀器連線"""
        try:
            if self.inst is not None:
                self.inst.close()
            if self.rm is not None:
                self.rm.close()
            LogHandler.log("Connection closed.")
        except Exception as e:
            LogHandler.log(f"[CLOSE] Error: {e}")

    def SET_Power_ON(self):
        """設定SG for RF Output ON"""
        try:
            # 設定頻率
            self.inst.write(f"OUTP ON")
            time.sleep(1)  # 等待設備響應
            LogHandler.log(f"PSW : OUTP ON")

        except Exception as e:
            LogHandler.log(f"[PSW : OUTP ON] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def SET_Power_OFF(self):
        """設定SG for RF Output OFF"""
        try:
            # 設定頻率
            self.inst.write(f"OUTP OFF")
            time.sleep(1)  # 等待設備響應
            LogHandler.log(f"PSW : OUTP OFF")

        except Exception as e:
            LogHandler.log(f"[PSW : OUTP OFF] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def is_number_regex(self, s):
        return bool(re.match(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$', s))
                  
        
# 使用範例
if __name__ == "__main__":
    LogHandler.log("EVM Instrument Test")
    