import time
import max30100
from signal import signal, SIGTERM, SIGHUP, pause

mx30 = max30100.MAX30100()
mx30.enable_spo2()

pulse = 0
oxygen = 0

def get_hb2_spo2():
    global pulse, oxygen
    
    mx30.read_sensor()
    mx30.ir, mx30.red
    hb = int (mx30.ir/100)
    spo2 = int(mx30.red/100)
    spo2 = spo2-3

    if mx30.ir != mx30.buffer_ir :
        pulse = hb
        
    if mx30.red != mx30.buffer_red :
        if spo2<=15:
            spo2=8
        if spo2>=101:
            spo2=99
        oxygen = spo2
    
    print("Detak Jantung: ",hb,", Oksigen Tubuh: ", spo2)
    time.sleep(0.5)#delay spo2
    return [pulse, oxygen]