# main.py
import datetime
import time
import flet as ft
import os
from test_sequency import test_seq
from fileHandler import FileHandler
from logHandler import LogHandler
from os import listdir
from os.path import isfile, isdir

def main(page: ft.Page):
    # ---------------- Page Setup ----------------
    page.title = "JIO Function Test Bundle v1.0.0.0"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 850
    page.window_height = 1100
    page.window_center()
    page.window_resizable = False

    # ---------------- Constants ----------------
    CELL_HEIGHT = 50
    HEADER_HEIGHT = 50
    DISPLAY_WINDOW_SIZE = 12

    column_widths = {
        "main": 200,
        "sub": 200,
        "lower": 100,
        "value": 100,
        "upper": 100,
        "result": 80
    }

    all_data = []
    all_data.append(["main_test_item_name", "sub_test_item_name", "lower_limit", "test_value", "upper_limit", "result"])
    list_view = ft.ListView(
        spacing=0,
        expand=True,
        auto_scroll=True
    )

    # ---------------- UI Builders ----------------
    def fixed_cell(text, width, is_result=False):
        text_style = ft.Text(
            text,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
            selectable=False,
            size=12
        )
        if is_result:
            if text.upper() == "PASS":
                text_style.color = ft.colors.GREEN
            elif text.upper() == "FAIL":
                text_style.color = ft.colors.RED
                text_style.weight = "bold"
            elif text.upper() == "LOG":
                text_style.color = ft.colors.WHITE

        return ft.Container(
            width=width,
            height=CELL_HEIGHT,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.GREY_700),
            content=ft.Tooltip(message=text, content=text_style)
        )

    def header_cell(text, width):
        return ft.Container(
            width=width,
            height=HEADER_HEIGHT,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_900,
            border=ft.border.all(1, ft.colors.GREY_700),
            content=ft.Text(text, weight="bold", color=ft.colors.WHITE)
        )

    def build_row(item):
        return ft.Row(
            controls=[
                fixed_cell(item["main"], column_widths["main"]),
                fixed_cell(item["sub"], column_widths["sub"]),
                fixed_cell(item["lower"], column_widths["lower"]),
                fixed_cell(item["value"], column_widths["value"]),
                fixed_cell(item["upper"], column_widths["upper"]),
                fixed_cell(item["result"], column_widths["result"], is_result=True),
            ],
            spacing=0
        )

    # ---------------- Event Handler ----------------
    def on_text_change(e):
        text_field.autofocus = False
        input_text = e.control.value
        start_time = time.time()

        status_text.value = " T E S T I N G "
        status_text.color = ft.colors.YELLOW
        status_text.update()

        #text_field.disabled = True
        text_field.update()

        #table_rows.rows.clear()
        #table_rows.update()

        list_view.clean()
        list_view.auto_scroll = True
        list_view.update()

        # Initialize the filename with current date and time
        today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))       
        tmp_time = f'{e.control.value}_{today.strftime("%Y%m%d-%H%M%S")}'
        tmp_path = f'{os.getcwd()}/log/Jio_L2_RF'
        isExist = os.path.exists(tmp_path)
        if not isExist:
            os.makedirs(tmp_path)        
        LogHandler.set_logfile(f"{tmp_path}/{tmp_time}.log")

        try: 
            main_seq = test_seq()
            test_result = main_seq.initialize(list_view, all_data, build_row, DISPLAY_WINDOW_SIZE)
            print(f"test_result = {test_result}")
            LogHandler.log(f"-------------------------------------------------------------------------------------------------------")
            LogHandler.log(f"test_result = main_seq.initialize = {test_result}")
            #for i in range(1, 101):
            if test_result:
                test_result = main_seq.add_data(list_view, all_data, build_row, DISPLAY_WINDOW_SIZE)
            LogHandler.log("Test END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except Exception as e:
            test_result = False
        
        elapsed_time = time.time() - start_time
        main_seq.add_time_data(list_view, all_data, build_row, elapsed_time, DISPLAY_WINDOW_SIZE)
        
        total_result = "FAIL"
        if test_result is True:
            status_text.value = "P A S S"
            status_text.color = ft.colors.GREEN
            status_text.update()
            total_result = "Pass"
        else:
            status_text.value = "F A I L"
            status_text.color = ft.colors.RED
            status_text.update()

        ## ---------- Finally Result ---------- ##
        tmp_path = f'{os.getcwd()}/Result/{total_result}/{tmp_time}'
        isExist = os.path.exists(tmp_path)
        if not isExist:
            os.makedirs(tmp_path)
        filename = f'{tmp_path}/{tmp_time}_Result.csv'
        FileHandler.csvFile(filename, all_data,'a')
        
        
        #text_field.disabled = False
        text_field.value=""
        time.sleep(1)
        text_field.autofocus = True
        text_field.update()
        text_field.focus()
        text_field.focus()

    # ---------------- UI Controls ----------------
    status_text = ft.Text("Hello", color=ft.colors.CYAN_200, size=100)
    text_field = ft.TextField(
        label="Enter SN with Barcode Scanner!!",
        on_submit=on_text_change,
        autofocus=True,
        bgcolor=ft.colors.GREY_800,
        color=ft.colors.WHITE,
        border_color=ft.colors.GREY_700
    )

    input_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    status_text,
                    text_field
                ],
                spacing=10
            ),
            padding=20
        )
    )

    table_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            header_cell("Main Test Item Name", column_widths["main"]),
                            header_cell("Sub Test Item Name", column_widths["sub"]),
                            header_cell("Lower Limit", column_widths["lower"]),
                            header_cell("Test Value", column_widths["value"]),
                            header_cell("Upper Limit", column_widths["upper"]),
                            header_cell("Result", column_widths["result"]),
                        ],
                        spacing=0,
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    ft.Container(
                        height=650,
                        content=list_view,
                        expand=False,
                        border=ft.border.only(bottom=ft.BorderSide(2, ft.colors.GREY_700))
                    )
                ],
                spacing=0
            ),
            padding=10
        )
    )

    page.add(ft.Column(controls=[input_card, table_card], spacing=20))

ft.app(target=main)