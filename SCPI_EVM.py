import time
import random

COMMAND = "FETC:WLAN:MEAS:MEV:MOD:AVER?"
TIMEOUT_SEC = 10
POLL_INTERVAL = 0.5

def mock_instrument_response():
    # 模擬儀器回應，有 30% 機率回傳 "RDY"，否則回傳 "BUSY"
    return "RDY" if random.random() < 0.3 else "BUSY"

def wait_for_ready(command, timeout_sec=5, poll_interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        print(f"Time : {time.time() - start_time}")
        # 模擬送指令
        print(f"送出指令: {command}")
        response = mock_instrument_response()
        print(f"收到回應: {response}")
        if response == "RDY":
            print("儀器已就緒，可以進行下一步！")
            return True
        time.sleep(poll_interval)
    print("等待逾時，未收到 RDY，流程中斷。")
    return False

def main():
    if wait_for_ready(COMMAND, TIMEOUT_SEC, POLL_INTERVAL):
        print("繼續後續流程...")
    else:
        print("終止程序。")

if __name__ == "__main__":
    main()
