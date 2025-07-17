import configparser
from logHandler import LogHandler

class test_seq:
    USER_MARGIN = {
        'tx_ch': 5,
        'rx_ch': 10,
        'tx_all': 5,
        'rx_all': 10
    }

    def __init__(self, config_path='testconfig.ini'):
        self.all_data = []
        self.display_limit = 12
        self.list_view = None

        # 讀取 config.ini
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.EVM_LIMITS = self._parse_limits('EVM_LIMITS')
        print(f"self.EVM_LIMITS : {self.EVM_LIMITS}")
        self.POWER_LIMITS = self._parse_limits('POWER_LIMITS')
        print(f"self.POWER_LIMITS : {self.POWER_LIMITS}")

        # 讀取儀器連線參數
        self.psw_address = self.config.get('INSTRUMENT', 'psw_address', fallback='ASRL6::INSTR')
        print(f"self.psw_address : {self.psw_address}")
        self.daq_address = self.config.get('INSTRUMENT', 'daq_address', fallback='USB-4711A,BID#0')
        print(f"self.daq_address : {self.daq_address}")
        self.evm_address = self.config.get('INSTRUMENT', 'evm_address', fallback='TCPIP0::192.168.200.50::inst0::INSTR')
        print(f"self.evm_address : {self.evm_address}")

    def _parse_limits(self, section):
        limits = {}
        if section in self.config:
            for key in self.config[section]:
                val = self.config[section][key]
                try:
                    lower, upper = map(float, val.split(','))
                    limits[key] = (lower, upper)
                except Exception as e:
                    LogHandler.log(f"Error parsing {section} for {key}: {e}")
        return limits

    def log_and_update(self, item, all_data, list_view, build_row):
        all_data.append([item["main"], item["sub"], item["lower"], item["value"], item["upper"], item["result"]])
        list_view.controls.append(build_row(item))
        list_view.auto_scroll = True
        list_view.update()

    def safe_shutdown(self):
        if hasattr(self, 'evm_instrument'):
            self.evm_instrument.SET_SG_OFF()
        if hasattr(self, 'daq'):
            self.daq.set_Power_OFF()
        if hasattr(self, 'psw'):
            self.psw.SET_Power_OFF()

    def initialize(self, list_view, all_data, build_row, display_limit=12):
        try:
            tmp_item = ""
            tmp_result_EVM = False

            import PSW
            tmp_item = "PSW"
            self.psw = PSW.PSW()
            tmp_result_psw = self.psw.INIT(self.psw_address)
            if tmp_result_psw:
                import USB_4711A_JIO
                tmp_item = "DAQ_4711A"
                self.daq = USB_4711A_JIO.DAQ_4711()
                tmp_result_4711 = self.daq.INIT(self.daq_address)
                if tmp_result_4711:
                    import Dut_control
                    self.jio_ftdi = Dut_control.Jio_ftdi()
                if tmp_result_4711:
                    tmp_item = "R&S_CMP180"
                    import RS_CMP180
                    self.evm_instrument = RS_CMP180.EVMInstrument()
                    tmp_result_EVM = self.evm_instrument.INIT(self.evm_address)
                    LogHandler.log(f"=======tmp_result_EVM : {tmp_result_EVM}")

            if tmp_result_EVM:
                return True
            else:
                item = {
                    "main": "JIO_L2_OnePanel_Error",
                    "sub": "Critical Initial Error",
                    "lower": " ",
                    "value": tmp_item,
                    "upper": " ",
                    "result": "FAIL",
                }
                self.log_and_update(item, all_data, list_view, build_row)
                return False
        except Exception as e:
            LogHandler.log(f"Error initialize : {e}")
            item = {
                "main": "JIO_L2_OnePanel_Error",
                "sub": "Critical Error",
                "lower": " ",
                "value": str(e),
                "upper": " ",
                "result": "FAIL",
            }
            self.log_and_update(item, all_data, list_view, build_row)
            self.safe_shutdown()
            return False

    def test_loop(self, mode, evm_key, power_key, user_margin, set_daq, set_dut, set_sg, all_data, list_view, build_row, set_channel, off_channel):
        set_daq()
        set_dut()
        self.evm_instrument.SET_SG(set_sg)
        evm_lower, evm_upper = self.EVM_LIMITS[evm_key]
        power_lower, power_upper = self.POWER_LIMITS[power_key]
        for i_chain in range(1, 3):
            for i_ic in range(1, 5):
                for i_ch in range(1, 5):
                    # 開啟 channel
                    set_channel(i_chain, i_ic, i_ch)
                    # 測試
                    self.evm_instrument.SET_EVM(10, user_margin)
                    tmp = self.evm_instrument.GET_EVM()
                    i_ch_evm = round(tmp[0], 3)
                    i_ch_power = round(tmp[1], 3)
                    i_ch_evm_result = "Pass" if evm_lower <= i_ch_evm <= evm_upper else "FAIL"
                    i_ch_power_result = "Pass" if power_lower <= i_ch_power <= power_upper else "FAIL"
                    # EVM
                    item_evm = {
                        "main": f"JIO_L2_OnePanel_{mode}_EVM",
                        "sub": f"Chain{i_chain}_IC{i_ic}_Channel{i_ch}",
                        "lower": evm_lower,
                        "value": i_ch_evm,
                        "upper": evm_upper,
                        "result": i_ch_evm_result,
                    }
                    self.log_and_update(item_evm, all_data, list_view, build_row)
                    # Power
                    item_power = {
                        "main": f"JIO_L2_OnePanel_{mode}_Power",
                        "sub": f"Chain{i_chain}_IC{i_ic}_Channel{i_ch}",
                        "lower": power_lower,
                        "value": i_ch_power,
                        "upper": power_upper,
                        "result": i_ch_power_result,
                    }
                    self.log_and_update(item_power, all_data, list_view, build_row)
                    # 關閉 channel
                    off_channel(i_chain, i_ic, i_ch)
                    if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
                        LogHandler.log(f"Fail detected at Chain{i_chain}_IC{i_ic}_Channel{i_ch}，停止測試")
                        self.end_test()
                        return False
        return True

    # Preset Table 單次測試
    def preset_table_test(self, mode, evm_key, power_key, user_margin, set_daq, set_dut, set_sg, build_row, all_data, list_view, sub_name):
        set_daq()
        set_dut()
        self.evm_instrument.SET_SG(set_sg)
        evm_lower, evm_upper = self.EVM_LIMITS[evm_key]
        power_lower, power_upper = self.POWER_LIMITS[power_key]
        self.evm_instrument.SET_EVM(10, user_margin)
        tmp = self.evm_instrument.GET_EVM()
        i_ch_evm = round(tmp[0], 3)
        i_ch_power = round(tmp[1], 3)
        i_ch_evm_result = "Pass" if evm_lower <= i_ch_evm <= evm_upper else "FAIL"
        i_ch_power_result = "Pass" if power_lower <= i_ch_power <= power_upper else "FAIL"
        # EVM
        item_evm = {
            "main": f"JIO_L2_OnePanel_{mode}_EVM",
            "sub": sub_name,
            "lower": evm_lower,
            "value": i_ch_evm,
            "upper": evm_upper,
            "result": i_ch_evm_result,
        }
        self.log_and_update(item_evm, all_data, list_view, build_row)
        # Power
        item_power = {
            "main": f"JIO_L2_OnePanel_{mode}_Power",
            "sub": sub_name,
            "lower": power_lower,
            "value": i_ch_power,
            "upper": power_upper,
            "result": i_ch_power_result,
        }
        self.log_and_update(item_power, all_data, list_view, build_row)
        if i_ch_evm_result == "FAIL" or i_ch_power_result == "FAIL":
            LogHandler.log(f"Fail detected at {mode} Preset table test，停止測試")
            self.end_test()
            return False
        return True

    def add_data(self, list_view, all_data, build_row, display_limit=12):
        try:
            self.psw.SET_Power_ON()
            self.daq.set_Power_On()

            # Tx_H
            self.evm_instrument.switch_SG('1.1')
            self.evm_instrument.switch_SA('1.6')
            self.evm_instrument.SET_SG_ON()
            if not self.test_loop(
                mode="Tx_H",
                evm_key='tx_h_ch',
                power_key='tx_h_ch',
                user_margin=self.USER_MARGIN['tx_ch'],
                set_daq=self.daq.set_Tx_H,
                set_dut=lambda: (self.jio_ftdi.ud_att_tx(50), self.jio_ftdi.channel_disable_all()),
                set_sg=-20,
                all_data=all_data,
                list_view=list_view,
                build_row=build_row,
                set_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 0, 0, 0, 0, 0, 0),
                off_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 0, 0, 1, 0, 0, 0)
            ):
                return False

            # Tx_V
            self.daq.set_Tx_V()
            if not self.test_loop(
                mode="Tx_V",
                evm_key='tx_v_ch',
                power_key='tx_v_ch',
                user_margin=self.USER_MARGIN['tx_ch'],
                set_daq=self.daq.set_Tx_V,
                set_dut=lambda: (self.jio_ftdi.ud_att_tx(50), self.jio_ftdi.channel_disable_all()),
                set_sg=-20,
                all_data=all_data,
                list_view=list_view,
                build_row=build_row,
                set_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 0, 1, 0, 0, 0, 0),
                off_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 0, 1, 1, 0, 0, 0)
            ):
                return False

            # Rx_H
            self.evm_instrument.SET_SG_OFF()
            self.evm_instrument.switch_SG('1.6')
            self.evm_instrument.switch_SA('1.1')
            self.evm_instrument.SET_SG_ON()
            if not self.test_loop(
                mode="Rx_H",
                evm_key='rx_h_ch',
                power_key='rx_h_ch',
                user_margin=self.USER_MARGIN['rx_ch'],
                set_daq=self.daq.set_Rx_H,
                set_dut=lambda: (self.jio_ftdi.ud_att_rx(50), self.jio_ftdi.channel_disable_all()),
                set_sg=0,
                all_data=all_data,
                list_view=list_view,
                build_row=build_row,
                set_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 1, 0, 0, 0, 0, 0),
                off_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 1, 0, 1, 0, 0, 0)
            ):
                return False

            # Rx_V
            self.daq.set_Rx_V()
            if not self.test_loop(
                mode="Rx_V",
                evm_key='rx_v_ch',
                power_key='rx_v_ch',
                user_margin=self.USER_MARGIN['rx_ch'],
                set_daq=self.daq.set_Rx_V,
                set_dut=lambda: (self.jio_ftdi.ud_att_rx(50), self.jio_ftdi.channel_disable_all()),
                set_sg=0,
                all_data=all_data,
                list_view=list_view,
                build_row=build_row,
                set_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 1, 1, 0, 0, 0, 0),
                off_channel=lambda i_chain, i_ic, i_ch: self.jio_ftdi.channel_setting(i_chain, i_ic, i_ch, 1, 1, 1, 0, 0, 0)
            ):
                return False

            # Preset Table Tx_H
            self.evm_instrument.switch_SG('1.1')
            self.evm_instrument.switch_SA('1.5')
            self.evm_instrument.SET_SG_ON()
            if not self.preset_table_test(
                mode="Tx_H",
                evm_key='tx_h_all',
                power_key='tx_h_all',
                user_margin=self.USER_MARGIN['tx_all'],
                set_daq=self.daq.set_Tx_H,
                set_dut=lambda: (self.jio_ftdi.channel_disable_all(), self.jio_ftdi.ud_att_tx(100), self.jio_ftdi.bfic_att(0, 0, 0)),
                set_sg=-16,
                build_row=build_row,
                all_data=all_data,
                list_view=list_view,
                sub_name="Phase_Preset"
            ):
                return False
            self.jio_ftdi.channel_disable_all()

            # Preset Table Tx_V
            self.daq.set_Tx_V()
            if not self.preset_table_test(
                mode="Tx_V",
                evm_key='tx_v_all',
                power_key='tx_v_all',
                user_margin=self.USER_MARGIN['tx_all'],
                set_daq=self.daq.set_Tx_V,
                set_dut=lambda: (self.jio_ftdi.channel_disable_all(), self.jio_ftdi.ud_att_tx(100), self.jio_ftdi.bfic_att(1, 0, 0)),
                set_sg=-16,
                build_row=build_row,
                all_data=all_data,
                list_view=list_view,
                sub_name="Phase_Preset"
            ):
                return False
            self.jio_ftdi.channel_disable_all()
            self.evm_instrument.SET_SG_OFF()

            # Preset Table Rx_H
            self.evm_instrument.switch_SG('1.6')
            self.evm_instrument.switch_SA('1.1')
            self.evm_instrument.SET_SG_ON()
            if not self.preset_table_test(
                mode="Rx_H",
                evm_key='rx_h_all',
                power_key='rx_h_all',
                user_margin=self.USER_MARGIN['rx_all'],
                set_daq=self.daq.set_Rx_H,
                set_dut=lambda: (self.jio_ftdi.channel_disable_all(), self.jio_ftdi.ud_att_rx(100), self.jio_ftdi.bfic_att(0, 0, 0)),
                set_sg=-4,
                build_row=build_row,
                all_data=all_data,
                list_view=list_view,
                sub_name="Phase_Preset"
            ):
                return False
            self.jio_ftdi.channel_disable_all()

            # Preset Table Rx_V
            self.daq.set_Rx_V()
            if not self.preset_table_test(
                mode="Rx_V",
                evm_key='rx_v_all',
                power_key='rx_v_all',
                user_margin=self.USER_MARGIN['rx_all'],
                set_daq=self.daq.set_Rx_V,
                set_dut=lambda: (self.jio_ftdi.channel_disable_all(), self.jio_ftdi.ud_att_rx(100), self.jio_ftdi.bfic_att(1, 0, 0)),
                set_sg=-4,
                build_row=build_row,
                all_data=all_data,
                list_view=list_view,
                sub_name="Phase_Preset"
            ):
                return False
            self.jio_ftdi.channel_disable_all()
            self.evm_instrument.SET_SG_OFF()

            self.daq.set_Power_OFF()
            self.psw.SET_Power_OFF()
            LogHandler.log(f'finished test sequency')
            return True

        except Exception as e:
            LogHandler.log(f"Error for testing: {e}")
            item = {
                "main": "JIO_L2_OnePanel_Error",
                "sub": "Critical Error",
                "lower": " ",
                "value": str(e),
                "upper": " ",
                "result": "FAIL",
            }
            self.log_and_update(item, all_data, list_view, build_row)
            self.safe_shutdown()
            return False

    def add_time_data(self, list_view, all_data, build_row, cycle_time, display_limit=12):
        item = {
            "main": "Test Cycle Time",
            "sub": "Total(sec)",
            "lower": " ",
            "value": f"{cycle_time:.3f}",
            "upper": " ",
            "result": "Log",
        }
        self.log_and_update(item, all_data, list_view, build_row)

    def end_test(self):
        self.safe_shutdown()
