import configparser
from Automation.BDaq import *
from Automation.BDaq.InstantDoCtrl import InstantDoCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
import flet as ft
import time

# 讀取 testconfig.ini
config = configparser.ConfigParser()
config.read('testconfig.ini')
daq_address = config.get('INSTRUMENT', 'daq_address', fallback='USB-4711A,BID#0')

profilePath = u"USB-4711A.xml"
do_states = [0, 0, 0, 0, 0, 0, 0, 0]
log_messages = []
page = None

def WriteDigital(device, profile, do_states):
    """寫入數位輸出"""
    try:
        instantDoCtrl = InstantDoCtrl(device)
        instantDoCtrl.loadProfile = profile
    except Exception as e:
        log_message(f"無法打開 DAQ 設備: {e}")
        return -1

    output_value = sum(state << index for index, state in enumerate(do_states))
    log_message(f"output_value = {output_value}")

    ret = instantDoCtrl.writeAny(0, 1, [output_value])
    instantDoCtrl.dispose()

    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        log_message(f"發生錯誤。最後的錯誤代碼: {ret.value:#x}. [{enumStr}]")
    else:
        log_message(f"數位輸出寫入完成: {format(output_value, '08b')}")

def set_do_state(index, value):
    global do_states
    do_states[index] = value
    WriteDigital(daq_address, profilePath, do_states) 

def clear_log():
    log_messages.clear()
    update_log_display()

def set_Tx_H():
    clear_log()
    set_do_state(0, 1)
    set_do_state(1, 0)
    time.sleep(0.5)
    set_do_state(6, 0)
    set_do_state(7, 0)
    log_message("Tx_H 設置完成")

def set_Tx_V():
    clear_log()
    set_do_state(0, 1)
    set_do_state(1, 0)
    time.sleep(0.5)
    set_do_state(6, 1)
    set_do_state(7, 0)
    log_message("T_V 設置完成")

def set_Rx_H():
    clear_log()
    set_do_state(0, 0)
    set_do_state(1, 1)
    set_do_state(6, 0)
    set_do_state(7, 1)
    log_message("Rx_H 設置完成")

def set_Rx_V():
    clear_log()
    set_do_state(0, 0)
    set_do_state(1, 1)
    set_do_state(6, 1)
    set_do_state(7, 1)
    log_message("Rx_V 設置完成")

def set_Power_On():
    clear_log()
    set_do_state(0, 0)
    set_do_state(1, 0)
    set_do_state(5, 1)
    time.sleep(0.5)
    set_do_state(4, 1)
    time.sleep(0.5)
    set_do_state(2, 1)
    time.sleep(0.5)
    set_do_state(3, 1)
    time.sleep(1)
    log_message("Power ON 設置完成")

def set_Power_OFF():
    clear_log()
    set_do_state(0, 0)
    set_do_state(1, 0)
    set_do_state(3, 0)
    set_do_state(2, 0)
    set_do_state(4, 0)
    set_do_state(5, 0)
    log_message("Power OFF 設置完成")

def log_message(message):
    log_messages.append(message)
    update_log_display()

def update_log_display():
    log_area.controls.clear()
    for msg in log_messages:
        log_area.controls.append(ft.Text(msg))
    page.update()

def main(p: ft.Page):
    global log_area, page
    page = p
    page.title = "數位輸出控制"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.window_width = 300
    page.window_height = 800

    button_width = 290

    button_tx = ft.ElevatedButton("設定 Tx_H", width=button_width, on_click=lambda e: set_Tx_H())
    button_rx = ft.ElevatedButton("設定 Tx_V", width=button_width, on_click=lambda e: set_Tx_V())
    button_h = ft.ElevatedButton("設定 Rx_H", width=button_width, on_click=lambda e: set_Rx_H())
    button_v = ft.ElevatedButton("設定 Rx_V", width=button_width, on_click=lambda e: set_Rx_V())
    button_power_on = ft.ElevatedButton("設定 POWER : On", width=button_width, on_click=lambda e: set_Power_On())
    button_power_off = ft.ElevatedButton("設定 POWER : OFF", width=button_width, on_click=lambda e: set_Power_OFF())

    button_group = ft.Column(
        controls=[
            button_tx,
            button_rx,
            button_h,
            button_v,
            button_power_on,
            button_power_off,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    log_area = ft.Column(
        controls=[],
        width=250,
        height=700,
        scroll=True,
        spacing=5,
    )

    page.add(button_group, log_area)

if __name__ == '__main__':
    print("配置文件加載成功。")
    ft.app(target=main)
