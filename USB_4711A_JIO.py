from Automation.BDaq import *
from Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
import time
from logHandler import LogHandler

#deviceDescription = "USB-4711A,BID#0"
profilePath = u"USB-4711A.xml"

# 初始的 do_states
do_states = [0, 0, 0, 0, 0, 0, 0, 0]
LogHandler.logs = []  # 用來儲存日誌訊息
page = None  # 定義全局變數 page

class DAQ_4711:

    def __init__(self):
        pass

    def INIT(self, deviceDescription):
        tmp_result = self.WriteDigital(deviceDescription, profilePath, do_states)
        self.deviceDescription = deviceDescription
        time.sleep(1)
        return tmp_result

    def WriteDigital(self, device, profile, do_states):
        """寫入數位輸出"""
        try:
            instantDoCtrl = InstantDoCtrl(device)
            instantDoCtrl.loadProfile = profile
        except Exception as e:
            LogHandler.log(f"無法打開 DAQ 設備: {e}")
            return False

        # 將陣列轉換為 output_value
        output_value = sum(state << index for index, state in enumerate(do_states))
        LogHandler.log(f"output_value = {output_value}")

        # 寫入數位數據
        ret = instantDoCtrl.writeAny(0, 1, [output_value])

        instantDoCtrl.dispose()

        if BioFailed(ret):
            enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
            LogHandler.log(f"發生錯誤。最後的錯誤代碼: {ret.value:#x}. [{enumStr}]")
        else:
            LogHandler.log(f"數位輸出寫入完成: {format(output_value, '08b')}")
        
        return True

    def set_do_state(self, index, value):
        """設置指定位置的數位輸出狀態並寫入"""
        global do_states
        do_states[index] = value  # 更新指定位置的值
        self.WriteDigital(self.deviceDescription, profilePath, do_states)


    def set_Tx_H(self):
        # Tx mode
        self.set_do_state(0, 1)  # 設置 DO 0 為 1
        self.set_do_state(1, 0)  # 設置 DO 1 為 0
        time.sleep(0.5)
        self.set_do_state(6, 0)  # 設置 DO 6 為 0
        self.set_do_state(7, 0)  # 設置 DO 7 為 0
        LogHandler.log("Tx_H 設置完成")

    def set_Tx_V(self):
        self.set_do_state(0, 1)  # 設置 DO 0 為 1
        self.set_do_state(1, 0)  # 設置 DO 1 為 0
        time.sleep(0.5)
        self.set_do_state(6, 1)  # 設置 DO 6 為 1
        self.set_do_state(7, 0)  # 設置 DO 7 為 0
        LogHandler.log("Tx_V 設置完成")

    def set_Rx_H(self):
        self.set_do_state(0, 0)  # 設置 DO 0 為 0
        self.set_do_state(1, 1)  # 設置 DO 1 為 1
        time.sleep(0.5)
        self.set_do_state(6, 0)  # 設置 DO 6 為 0
        self.set_do_state(7, 1)  # 設置 DO 7 為 1
        LogHandler.log("Rx_H 設置完成")

    def set_Rx_V(self):
        self.set_do_state(0, 0)  # 設置 DO 0 為 0
        self.set_do_state(1, 1)  # 設置 DO 1 為 1
        time.sleep(0.5)
        self.set_do_state(6, 1)  # 設置 DO 6 為 1
        self.set_do_state(7, 1)  # 設置 DO 7 為 1
        LogHandler.log("Rx_V 設置完成")

    def set_Power_On(self):
        # Standby mode
        self.set_do_state(0, 0)  # 設置 DO 0 為 0
        self.set_do_state(1, 0)  # 設置 DO 1 為 0
        # Power ON sequency
        self.set_do_state(5, 1)  # 設置 DO 5 為 1
        time.sleep(0.5)
        self.set_do_state(4, 1)  # 設置 DO 4 為 1
        time.sleep(0.5)
        self.set_do_state(2, 1)  # 設置 DO 2 為 1
        time.sleep(0.5)
        self.set_do_state(3, 1)  # 設置 DO 3 為 1
        time.sleep(1)
        LogHandler.log("Power ON 設置完成")

    def set_Power_OFF(self):
        # Standby mode
        self.set_do_state(0, 0)  # 設置 DO 0 為 0
        self.set_do_state(1, 0)  # 設置 DO 1 為 0
        # Power ON sequency
        self.set_do_state(3, 0)  # 設置 DO 5 為 1
        self.set_do_state(2, 0)  # 設置 DO 4 為 1
        self.set_do_state(4, 0)  # 設置 DO 2 為 1
        self.set_do_state(5, 0)  # 設置 DO 3 為 1
        LogHandler.log("Power OFF 設置完成")

if __name__ == '__main__':
    LogHandler.log("配置文件加載成功。")


