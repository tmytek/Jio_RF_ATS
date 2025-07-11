import pyvisa
import sys
import time
import re
from logHandler import LogHandler

class EVMInstrument:
    
    def __init__(self):
        self.rm = None
        self.inst = None

    def INIT(self, resource_str):
        """初始化儀器連線，並設定WLAN EVM單次量測"""
        try:
            self.rm = pyvisa.ResourceManager()
            self.inst = self.rm.open_resource(resource_str)
            idn = self.inst.query('*IDN?')
            LogHandler.log(f"*IDN?: {idn.strip()}")
            # 設定WLAN EVM單次量測，等待操作完成
            opc = self.inst.query("CONF:WLAN:MEAS:MEV:REP SING;*OPC?")
            LogHandler.log(f"CONF:WLAN:MEAS:MEV:REP SING, OPC: {opc.strip()}")
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

    def SET_SG_ON(self):
        """設定SG for RF Output ON"""
        try:
            # 設定頻率
            self.inst.write(f"SOUR:GPRF:GEN:STAT ON")
            LogHandler.log(f"SOUR:GPRF:GEN:STAT ON")

        except Exception as e:
            LogHandler.log(f"[SET_SG_ON] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def SET_SG_OFF(self):
        """設定SG for RF Output OFF"""
        try:
            # 設定頻率
            self.inst.write(f"SOUR:GPRF:GEN:STAT OFF")
            LogHandler.log(f"SOUR:GPRF:GEN:STAT OFF")

        except Exception as e:
            LogHandler.log(f"[SET_SG_OFF] Error: {e}")
            self.close()
            # sys.exit(1)

    def SET_SG(self, power_level):
        """設定SG for RF Output"""
        try:
            # 設定頻率
            self.inst.write(f"SOURce:GPRF:GEN:RFSettings:LEVel {power_level}")
            LogHandler.log(f"SOURce:GPRF:GEN:RFSettings:LEVel {power_level}")

        except Exception as e:
            LogHandler.log(f"[SET_SG] Error: {e}")
            self.close()
            # sys.exit(1)

    def SET_EVM(self, timeout_sec=5, user_margin=0):
        """設定儀器的 EVM 參數"""
        try:
            # setting user margin
            # CONFigure:WLAN:MEAS:RFSettings:UMARgin 0
            tmp = self.inst.query(f"CONF:WLAN:MEAS:RFS:UMARgin {user_margin};*OPC?")
            LogHandler.log(f"CONF:WLAN:MEAS:RFS:LRST, OPC: {tmp.strip()}")
            # Set 1 
            tmp = self.inst.query("CONF:WLAN:MEAS:RFS:LRST;*OPC?")
            LogHandler.log(f"CONF:WLAN:MEAS:RFS:LRST, OPC: {tmp.strip()}")
            # Set 2 
            tmp = self.inst.query("INIT:WLAN:MEAS:MEV;*OPC?")
            LogHandler.log(f"INIT:WLAN:MEAS:MEV, OPC: {tmp.strip()}")

            # Wait for "RDY"
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                LogHandler.log(f"Time : {time.time() - start_time}")
                # 模擬送指令
                response = self.inst.query("FETC:WLAN:MEAS:MEV:STAT?")
                LogHandler.log(f"FETC:WLAN:MEAS:MEV:STAT? : {response.strip()}")
                if response.strip() == "RDY":
                    LogHandler.log("儀器已就緒，可以進行下一步！")
                    return True
            LogHandler.log("等待逾時，未收到 RDY，流程中斷。")
            return False

        except Exception as e:
            LogHandler.log(f"[SET_EVM] Error: {e}")
            self.close()
            # sys.exit(1)

    def GET_EVM(self):
        """取得儀器目前的 EVM 量測值"""
        try:
            data_evm = self.inst.query("FETC:WLAN:MEAS:MEV:MOD:AVER?")
            #LogHandler.log(data_evm)
            
            data_list = [str(x) for x in data_evm.split(',')]
            #LogHandler.log(data_evm)
            LogHandler.log(data_list[15])
            LogHandler.log(data_list[12])
            LogHandler.log(self.is_number_regex(data_list[15]))

            if self.is_number_regex(data_list[15]):
                i_EVM = float(data_list[15])
            else:
                i_EVM = -999

            if self.is_number_regex(data_list[12]):
                i_Power = float(data_list[12])
            else:
                i_Power = -999
            
            if i_EVM > 0:
                i_EVM = 0
            if i_Power > 50:
                i_Power = -60
            LogHandler.log(f"EVM: {i_EVM}")
            LogHandler.log(f"i_Power: {i_Power}")
            return [i_EVM,i_Power]
        except Exception as e:
            LogHandler.log(f"[GET_EVM] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def switch_SG(self, rfport):
        try:
            # 設定 RF Port
            if '1.'in rfport:
                self.inst.write('ROUTe:GPRF:GEN:SPATh \'RF1.1-RF1.8\'')
            elif '2.'in rfport:
                self.inst.write('ROUTe:GPRF:GEN:SPATh \'RF2.1-RF2.8\'')
            else:
                    self.inst.write('ROUTe:GPRF:GEN:SPATh \'RF1.1-RF1.8\'')
            # 設定 RF Port 的使用情況
            if (rfport =='1.1')or(rfport =='2.1'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF;*OPC?') 
            elif (rfport =='1.2')or(rfport =='2.2'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF;*OPC?') 
            elif (rfport =='1.3')or(rfport =='2.3'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF;*OPC?') 
            elif (rfport =='1.4')or(rfport =='2.4'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,ON,OFF,OFF,OFF,OFF;*OPC?') 
            elif (rfport =='1.5')or(rfport =='2.5'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,OFF,ON,OFF,OFF,OFF;*OPC?') 
            elif (rfport =='1.6')or(rfport =='2.6'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,OFF,OFF,ON,OFF,OFF;*OPC?')  
            elif (rfport =='1.7')or(rfport =='2.7'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,OFF,OFF,OFF,ON,OFF;*OPC?')  
            elif (rfport =='1.8')or(rfport =='2.8'):
                    self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,OFF,OFF,OFF,OFF,ON;*OPC?')  
            else:
                self.inst.query('CONF:GPRF:GEN:SPAT:USAG OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF;*OPC?')          

        except Exception as e:
            LogHandler.log(f"[switch_SG] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def switch_SA(self, rfport):
        try:
            # 設定 RF Port
            # 'ROUT:WLAN:MEAS:SPATh \'RF' + str(VSA_RFPort) + '\';*OPC?'
            self.inst.write('ROUT:WLAN:MEAS:SPATh \'RF' + str(rfport) + '\';*OPC?')
            

        except Exception as e:
            LogHandler.log(f"[switch_SG] Error: {e}")
            self.close()
            # sys.exit(1)
    
    def is_number_regex(self, s):
        return bool(re.match(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$', s))
                  
        
# 使用範例
if __name__ == "__main__":
    LogHandler.log("EVM Instrument Test")
    