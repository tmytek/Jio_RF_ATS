# test_sequency.py
from logHandler import LogHandler
class test_seq:

    def __init__(self):
        self.all_data = []
        self.display_limit = 12
        self.list_view = None
        
    def initialize(self, list_view, all_data, build_row, display_limit=12):
        """
        try:
            import USB_4711A_JIO 
            self.daq = USB_4711A_JIO.DAQ_4711()
        except Exception as e:
            LogHandler.log(f"Error initializing USB_4711A_JIO: {e}")
        
        try:
            import Dut_control
            self.jio_ftdi = Dut_control.Jio_ftdi()
        except Exception as e:
            LogHandler.log(f"Error initializing Dut_control: {e}")
        
        try:
            import RS_CMP180
            self.evm_instrument = RS_CMP180.EVMInstrument()
            self.evm_instrument.INIT('TCPIP0::192.168.200.50::inst0::INSTR')
        except Exception as e:
            LogHandler.log(f"Error initializing RS_CMP180: {e}")

        """
        try:
            tmp_item = ""
            tmp_result_EVM = False

            import PSW
            tmp_item = "PSW"
            self.psw = PSW.PSW()
            tmp_result_psw = self.psw.INIT('ASRL6::INSTR')
            if tmp_result_psw:
                import USB_4711A_JIO 
                tmp_item = "DAQ_4711A"
                self.daq = USB_4711A_JIO.DAQ_4711()
                tmp_result_4711 = self.daq.INIT()
                if tmp_result_4711:
                    import Dut_control
                    self.jio_ftdi = Dut_control.Jio_ftdi()
                if tmp_result_4711:
                    tmp_item = "R&S_CMP180"    
                    import RS_CMP180
                    self.evm_instrument = RS_CMP180.EVMInstrument()
                    tmp_result_EVM = self.evm_instrument.INIT('TCPIP0::192.168.200.50::inst0::INSTR')
                    LogHandler.log(f"=======tmp_result_EVM : {tmp_result_EVM}")

            
            if tmp_result_EVM:
                return True
            else:
                item = {
                    "main": f"JIO_L2_OnePanel_Error",
                    "sub": f"Critical Initial Error",
                    "lower": " ",
                    "value": tmp_item,
                    "upper": " ",
                    "result": f"FAIL",
                }
                all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                # 建立新的資料列，並加入 ListView 控件
                list_view.controls.append(build_row(item))
                """
                # 只保留最後 N 筆顯示
                if len(list_view.controls) > display_limit:
                    list_view.controls.pop(0)
                """
                list_view.auto_scroll = True
                list_view.update()
        
        except Exception as e:
            LogHandler.log(f"Error initialize : {e}")
            item = {
                "main": f"JIO_L2_OnePanel_Error",
                "sub": f"Critical Error",
                "lower": " ",
                "value": tmp_item,
                "upper": " ",
                "result": f"FAIL",
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))
            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            if hasattr(self, 'evm_instrument'):
                self.evm_instrument.SET_SG_OFF()
            if hasattr(self, 'daq'):    
                self.daq.set_Power_OFF()
            
            return False

        
    def status_text_testing(status_text,ft):
        status_text = ft.Text("T E S T I N G", color=ft.colors.YELLOW, size=100)

    def add_data(self, list_view, all_data, build_row, display_limit=12):
        #for i in range(1, 1001):
        # parameters
        # channel criteria
        EVM_tx_h_ch_lower = -90
        EVM_tx_h_ch_higher = -10
        EVM_tx_v_ch_lower = -91
        EVM_tx_v_ch_higher = -11
        EVM_rx_h_ch_lower = -92
        EVM_rx_h_ch_higher = -12
        EVM_rx_v_ch_lower = -93
        EVM_rx_v_ch_higher = -13
        Power_tx_h_ch_lower = -94
        Power_tx_h_ch_higher = -14
        Power_tx_v_ch_lower = -95
        Power_tx_v_ch_higher = -15
        Power_rx_h_ch_lower = -96
        Power_rx_h_ch_higher = -16
        Power_rx_v_ch_lower = -97
        Power_rx_v_ch_higher = -17
        
        # Polarity check criteria
        EVM_tx_h_all_lower = -98
        EVM_tx_h_all_higher = -18
        EVM_tx_v_all_lower = -99
        EVM_tx_v_all_higher = -19
        EVM_rx_h_all_lower = -999
        EVM_rx_h_all_higher = -9
        EVM_rx_v_all_lower = -998
        EVM_rx_v_all_higher = -8
        Power_tx_h_all_lower = -997
        Power_tx_h_all_higher = -7
        Power_tx_v_all_lower = -996
        Power_tx_v_all_higher = -6
        Power_rx_h_all_lower = -995
        Power_rx_h_all_higher = -5
        Power_rx_v_all_lower = -994
        Power_rx_v_all_higher = -4

        # CMP180 user margin setting
        tx_ch_user_margin = 5
        rx_ch_user_margin = 10
        tx_all_user_margin = 5
        rx_all_user_margin = 10

        try:
            
            # Initialize instruments
            self.psw.SET_Power_ON()
            self.daq.set_Power_On()

            # ----- Tx Setting -----
            # SG RF On
            self.evm_instrument.switch_SG('1.1')
            self.evm_instrument.switch_SA('1.6')
            self.evm_instrument.SET_SG_ON()
            
            # ------ Tx_H test ------
            self.daq.set_Tx_H()
            # set DUT
            self.jio_ftdi.ud_att_tx(50)
            self.jio_ftdi.channel_disable_all()

            # set SG Power for Tx_H
            self.evm_instrument.SET_SG(-20)

            for i_chain in range(1, 3):
                for i_IC_no in range(1, 5):
                    for i_channel in range(1, 5):
                        # set channel and turn ON
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 0, 0, 0, 0, 0, 0)
                        # check EVM
                        self.evm_instrument.SET_EVM(10, tx_ch_user_margin)
                        tmp = self.evm_instrument.GET_EVM()
                        i_ch_evm = round(tmp[0], 3)
                        i_ch_power = round(tmp[1], 3)
                        i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_tx_h_ch_higher)and(i_ch_evm >= EVM_tx_h_ch_lower))  else "FAIL"
                        i_ch_power_result = "Pass" if ((i_ch_power <= Power_tx_h_ch_higher)and(i_ch_power >= Power_tx_h_ch_lower))  else "FAIL"
                        item = {
                            "main": f"JIO_L2_OnePanel_Tx_H_EVM",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": EVM_tx_h_ch_lower,
                            "value": i_ch_evm,
                            "upper": EVM_tx_h_ch_higher,
                            "result": i_ch_evm_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        list_view.controls.append(build_row(item))
                        item = {
                            "main": f"JIO_L2_OnePanel_Tx_H_Power",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": Power_tx_h_ch_lower,
                            "value": i_ch_power,
                            "upper": Power_tx_h_ch_higher,
                            "result": i_ch_power_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        # 建立新的資料列，並加入 ListView 控件
                        list_view.controls.append(build_row(item))

                        # turn OFF channel
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 0, 0, 1, 0, 0, 0)
                        """
                        # 只保留最後 N 筆顯示
                        if len(list_view.controls) > display_limit:
                            list_view.controls.pop(0)
                        """
                        list_view.auto_scroll = True
                        list_view.update()

                        if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                            LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                            self.end_test()
                            return False  # 直接結束

            # ------ Tx_V test ------
            self.daq.set_Tx_V()
            # set DUT
            self.jio_ftdi.ud_att_tx(50)
            self.jio_ftdi.channel_disable_all()

            # set SG Power for Tx_V
            self.evm_instrument.SET_SG(-20)

            for i_chain in range(1, 3):
                for i_IC_no in range(1, 5):
                    for i_channel in range(1, 5):
                        # set channel and turn ON
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 0, 1, 0, 0, 0, 0)
                        # check EVM
                        self.evm_instrument.SET_EVM(10, tx_ch_user_margin)
                        tmp = self.evm_instrument.GET_EVM()
                        i_ch_evm = round(tmp[0], 3)
                        i_ch_power = round(tmp[1], 3)
                        i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_tx_v_ch_higher)and(i_ch_evm >= EVM_tx_v_ch_lower))  else "FAIL"
                        i_ch_power_result = "Pass" if ((i_ch_power <= Power_tx_v_ch_higher)and(i_ch_power >= Power_tx_v_ch_lower))  else "FAIL"
                        item = {
                            "main": f"JIO_L2_OnePanel_Tx_V_EVM",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": EVM_tx_v_ch_lower,
                            "value": i_ch_evm,
                            "upper": EVM_tx_v_ch_higher,
                            "result": i_ch_evm_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        list_view.controls.append(build_row(item))
                        item = {
                            "main": f"JIO_L2_OnePanel_Tx_V_Power",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": Power_tx_v_ch_lower,
                            "value": i_ch_power,
                            "upper": Power_tx_v_ch_higher,
                            "result": i_ch_power_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        # 建立新的資料列，並加入 ListView 控件
                        list_view.controls.append(build_row(item))

                        # turn OFF channel
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 0, 1, 1, 0, 0, 0)
                        """
                        # 只保留最後 N 筆顯示
                        if len(list_view.controls) > display_limit:
                            list_view.controls.pop(0)
                        """
                        list_view.auto_scroll = True
                        list_view.update()

                        if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                            LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                            self.end_test()
                            return False  # 直接結束
            
            # turn OFF SG power for switching SG port ( Tx -> Rx )            
            self.evm_instrument.SET_SG_OFF()

            # ----- Rx Setting -----
            # SG RF On
            self.evm_instrument.switch_SG('1.6')
            self.evm_instrument.switch_SA('1.1')
            self.evm_instrument.SET_SG_ON()
            # ------ Rx_H test ------
            self.daq.set_Rx_H()
            # set DUT
            self.jio_ftdi.ud_att_rx(50)
            self.jio_ftdi.channel_disable_all()

            # set SG Power for Rx_H
            self.evm_instrument.SET_SG(0)

            for i_chain in range(1, 3):
                for i_IC_no in range(1, 5):
                    for i_channel in range(1, 5):
                        # set channel and turn ON
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 1, 0, 0, 0, 0, 0)
                        # check EVM
                        self.evm_instrument.SET_EVM(10, rx_ch_user_margin)
                        tmp = self.evm_instrument.GET_EVM()
                        i_ch_evm = round(tmp[0], 3)
                        i_ch_power = round(tmp[1], 3)
                        i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_rx_h_ch_higher)and(i_ch_evm >= EVM_rx_h_ch_lower))  else "FAIL"
                        i_ch_power_result = "Pass" if ((i_ch_power <= Power_rx_h_ch_higher)and(i_ch_power >= Power_rx_h_ch_lower))  else "FAIL"
                        item = {
                            "main": f"JIO_L2_OnePanel_Rx_H_EVM",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": EVM_rx_h_ch_lower,
                            "value": i_ch_evm,
                            "upper": EVM_rx_h_ch_higher,
                            "result": i_ch_evm_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        list_view.controls.append(build_row(item))
                        item = {
                            "main": f"JIO_L2_OnePanel_Rx_H_Power",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": Power_rx_h_ch_lower,
                            "value": i_ch_power,
                            "upper": Power_rx_h_ch_higher,
                            "result": i_ch_power_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        # 建立新的資料列，並加入 ListView 控件
                        list_view.controls.append(build_row(item))

                        # turn OFF channel
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 1, 0, 1, 0, 0, 0)
                        """
                        # 只保留最後 N 筆顯示
                        if len(list_view.controls) > display_limit:
                            list_view.controls.pop(0)
                        """
                        list_view.auto_scroll = True
                        list_view.update()

                        if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                            LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                            self.end_test()
                            return False  # 直接結束


            # ------ Rx_V test ------
            self.daq.set_Rx_V()
            # set DUT
            self.jio_ftdi.ud_att_rx(50)
            self.jio_ftdi.channel_disable_all()

            # set SG Power for Rx_V
            self.evm_instrument.SET_SG(0)

            for i_chain in range(1, 3):
                for i_IC_no in range(1, 5):
                    for i_channel in range(1, 5):
                        # set channel and turn ON
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 1, 1, 0, 0, 0, 0)
                        # check EVM
                        self.evm_instrument.SET_EVM(10, rx_ch_user_margin)
                        tmp = self.evm_instrument.GET_EVM()
                        i_ch_evm = round(tmp[0], 3)
                        i_ch_power = round(tmp[1], 3)
                        i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_rx_v_ch_higher)and(i_ch_evm >= EVM_rx_v_ch_lower))  else "FAIL"
                        i_ch_power_result = "Pass" if ((i_ch_power <= Power_rx_v_ch_higher)and(i_ch_power >= Power_rx_v_ch_lower))  else "FAIL"
                        item = {
                            "main": f"JIO_L2_OnePanel_Rx_V_EVM",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": EVM_rx_v_ch_lower,
                            "value": i_ch_evm,
                            "upper": EVM_rx_v_ch_higher,
                            "result": i_ch_evm_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        list_view.controls.append(build_row(item))
                        item = {
                            "main": f"JIO_L2_OnePanel_Rx_V_Power",
                            "sub": f"Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}",
                            "lower": Power_rx_v_ch_lower,
                            "value": i_ch_power,
                            "upper": Power_rx_v_ch_higher,
                            "result": i_ch_power_result,
                        }
                        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
                        # 建立新的資料列，並加入 ListView 控件
                        list_view.controls.append(build_row(item))

                        # turn OFF channel
                        self.jio_ftdi.channel_setting(i_chain, i_IC_no, i_channel, 1, 1, 1, 0, 0, 0)
                        """
                        # 只保留最後 N 筆顯示
                        if len(list_view.controls) > display_limit:
                            list_view.controls.pop(0)
                        """
                        list_view.auto_scroll = True
                        list_view.update()

                        if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                            LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                            self.end_test()
                            return False  # 直接結束

            # ----- Tx Setting -----
            # SG RF On
            self.evm_instrument.switch_SG('1.1')
            self.evm_instrument.switch_SA('1.5')
            self.evm_instrument.SET_SG_ON()
            # ------ Tx_H Preset table test ------
            self.daq.set_Tx_H()
            # set DUT
            self.jio_ftdi.channel_disable_all()
            self.jio_ftdi.ud_att_tx(50)
            self.jio_ftdi.bfic_att(0, 5, 5)
            
            # set SG Power for Tx_H
            self.evm_instrument.SET_SG(-20)
            # check EVM
            self.evm_instrument.SET_EVM(10, tx_all_user_margin)
            tmp = self.evm_instrument.GET_EVM()
            i_ch_evm = round(tmp[0], 3)
            i_ch_power = round(tmp[1], 3)
            i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_tx_h_all_higher)and(i_ch_evm >= EVM_tx_h_all_lower))  else "FAIL"
            i_ch_power_result = "Pass" if ((i_ch_power <= Power_tx_h_all_higher)and(i_ch_power >= Power_tx_h_all_lower))  else "FAIL"
            item = {
                "main": f"JIO_L2_OnePanel_Tx_H_EVM",
                "sub": f"Phase_Preset",
                "lower": EVM_tx_h_all_lower,
                "value": i_ch_evm,
                "upper": EVM_tx_h_all_higher,
                "result": i_ch_evm_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            list_view.controls.append(build_row(item))
            item = {
                "main": f"JIO_L2_OnePanel_Tx_H_Power",
                "sub": f"Phase_Preset",
                "lower": Power_tx_h_all_lower,
                "value": i_ch_power,
                "upper": Power_tx_h_all_higher,
                "result": i_ch_power_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))

            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            # Turn OFF all channel
            self.jio_ftdi.channel_disable_all()
            
            if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                LogHandler.log(f"Fail detected at Tx_H Preset table test，停止測試")
                self.end_test()
                return False  # 直接結束

            # ------ Tx_V Preset table test ------
            self.daq.set_Tx_V()
            # set DUT
            self.jio_ftdi.channel_disable_all()
            self.jio_ftdi.ud_att_tx(50)
            self.jio_ftdi.bfic_att(1, 5, 5)
            
            # set SG Power for Tx_H
            self.evm_instrument.SET_SG(-20)
            # check EVM
            self.evm_instrument.SET_EVM(10, tx_all_user_margin)
            tmp = self.evm_instrument.GET_EVM()
            i_ch_evm = round(tmp[0], 3)
            i_ch_power = round(tmp[1], 3)
            i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_tx_v_all_higher)and(i_ch_evm >= EVM_tx_v_all_lower))  else "FAIL"
            i_ch_power_result = "Pass" if ((i_ch_power <= Power_tx_v_all_higher)and(i_ch_power >= Power_tx_v_all_lower))  else "FAIL"
            item = {
                "main": f"JIO_L2_OnePanel_Tx_V_EVM",
                "sub": f"Phase_Preset",
                "lower": EVM_tx_v_all_lower,
                "value": i_ch_evm,
                "upper": EVM_tx_v_all_higher,
                "result": i_ch_evm_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            list_view.controls.append(build_row(item))
            item = {
                "main": f"JIO_L2_OnePanel_Tx_V_Power",
                "sub": f"Phase_Preset",
                "lower": Power_tx_v_all_lower,
                "value": i_ch_power,
                "upper": Power_tx_v_all_higher,
                "result": i_ch_power_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))

            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            # Turn OFF all channel
            self.jio_ftdi.channel_disable_all()
            self.evm_instrument.SET_SG_OFF()
            
            if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                LogHandler.log(f"Fail detected at Tx_V Preset table test，停止測試")
                self.end_test()
                return False  # 直接結束

            # ----- Rx Setting -----
            # SG RF On
            self.evm_instrument.switch_SG('1.6')
            self.evm_instrument.switch_SA('1.1')
            self.evm_instrument.SET_SG_ON()
            # ------ Rx_H Preset table test ------
            self.daq.set_Rx_H()
            # set DUT
            self.jio_ftdi.channel_disable_all()
            self.jio_ftdi.ud_att_rx(50)
            self.jio_ftdi.bfic_att(0, 5, 5)
            
            # set SG Power for Rx_H
            self.evm_instrument.SET_SG(0)
            # check EVM
            self.evm_instrument.SET_EVM(10, rx_all_user_margin)
            tmp = self.evm_instrument.GET_EVM()
            i_ch_evm = round(tmp[0], 3)
            i_ch_power = round(tmp[1], 3)
            i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_rx_h_all_higher)and(i_ch_evm >= EVM_rx_h_all_lower))  else "FAIL"
            i_ch_power_result = "Pass" if ((i_ch_power <= Power_rx_h_all_higher)and(i_ch_power >= Power_rx_h_all_lower))  else "FAIL"
            item = {
                "main": f"JIO_L2_OnePanel_Rx_H_EVM",
                "sub": f"Phase_Preset",
                "lower": EVM_rx_h_all_lower,
                "value": i_ch_evm,
                "upper": EVM_rx_h_all_higher,
                "result": i_ch_evm_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            list_view.controls.append(build_row(item))
            item = {
                "main": f"JIO_L2_OnePanel_Rx_H_Power",
                "sub": f"Phase_Preset",
                "lower": Power_rx_h_all_lower,
                "value": i_ch_power,
                "upper": Power_rx_h_all_higher,
                "result": i_ch_power_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))

            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            # Turn OFF all channel
            self.jio_ftdi.channel_disable_all()
            
            if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                self.end_test()
                return False  # 直接結束

            # ------ Rx_V Preset table test ------
            self.daq.set_Rx_V()
            # set DUT
            self.jio_ftdi.channel_disable_all()
            self.jio_ftdi.ud_att_rx(50)
            self.jio_ftdi.bfic_att(1, 5, 5)
            
            # set SG Power for Tx_H
            self.evm_instrument.SET_SG(0)
            # check EVM
            self.evm_instrument.SET_EVM(10, rx_all_user_margin)
            tmp = self.evm_instrument.GET_EVM()
            i_ch_evm = round(tmp[0], 3)
            i_ch_power = round(tmp[1], 3)
            i_ch_evm_result = "Pass" if ((i_ch_evm <= EVM_rx_v_all_higher)and(i_ch_evm >= EVM_rx_v_all_lower))  else "FAIL"
            i_ch_power_result = "Pass" if ((i_ch_power <= Power_rx_v_all_higher)and(i_ch_power >= Power_rx_v_all_lower))  else "FAIL"
            item = {
                "main": f"JIO_L2_OnePanel_Rx_V_EVM",
                "sub": f"Phase_Preset",
                "lower": EVM_rx_v_all_lower,
                "value": i_ch_evm,
                "upper": EVM_rx_v_all_higher,
                "result": i_ch_evm_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            list_view.controls.append(build_row(item))
            item = {
                "main": f"JIO_L2_OnePanel_Rx_V_Power",
                "sub": f"Phase_Preset",
                "lower": Power_rx_v_all_lower,
                "value": i_ch_power,
                "upper": Power_rx_v_all_higher,
                "result": i_ch_power_result,
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))

            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            # Turn OFF all channel
            self.jio_ftdi.channel_disable_all()
            
            if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_IC_no}_Channel{i_channel}，停止測試")
                self.end_test()
                return False  # 直接結束



            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()

            self.evm_instrument.SET_SG_OFF()
            self.daq.set_Power_OFF()
            self.psw.SET_Power_OFF()
            LogHandler.log(f'finished test sequency')
            return True


        except Exception as e:

            LogHandler.log(f"Error for testing: {e}")

            item = {
                "main": f"JIO_L2_OnePanel_Error",
                "sub": f"Critical Error",
                "lower": " ",
                "value": e,
                "upper": " ",
                "result": f"FAIL",
            }
            all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])
            # 建立新的資料列，並加入 ListView 控件
            list_view.controls.append(build_row(item))
            """
            # 只保留最後 N 筆顯示
            if len(list_view.controls) > display_limit:
                list_view.controls.pop(0)
            """
            list_view.auto_scroll = True
            list_view.update()
            if hasattr(self, 'evm_instrument'):
                self.evm_instrument.SET_SG_OFF()
            if hasattr(self, 'daq'):    
                self.daq.set_Power_OFF()
            if hasattr(self, 'psw'):
                self.psw.SET_Power_OFF()
            
            return False

    def add_time_data(self, list_view, all_data, build_row, cycle_time, display_limit=12):
        item = {
                "main": f"Test Cycle Time",
                "sub": f"Total(sec)",
                "lower": f" ",
                "value": f"{cycle_time:.3f}",
                "upper": f" ",
                "result": "Log",
            }

        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"], ])

        # 建立新的資料列，並加入 ListView 控件
        list_view.controls.append(build_row(item))

        """
        # 只保留最後 N 筆顯示
        if len(list_view.controls) > display_limit:
            list_view.controls.pop(0)
        """
            
        list_view.auto_scroll = True
        list_view.update()

    def end_test(self):
        if hasattr(self, 'evm_instrument'):
            self.evm_instrument.SET_SG_OFF()
        if hasattr(self, 'daq'):    
            self.daq.set_Power_OFF()
        if hasattr(self, 'psw'):
            self.psw.SET_Power_OFF()


    