from gpiozero import CPUTemperature
import psutil as p
import os
from time import sleep
from collections import namedtuple
class Monitor:
    @classmethod
    def get_cpu_info(cls):
        cpu_tuple = namedtuple('cpu', 'temp used')
        temp = CPUTemperature().temperature
        temp = float("{:.2f}".format(temp))
        used = p.cpu_percent()
        return cpu_tuple(temp, used)._asdict()
    @classmethod
    def get_ram_info(cls):
        ram_tuple = namedtuple('ram', 'total free used free_pr used_pr')
        total = int(p.virtual_memory().total/(pow(1024, 2)))
        available = int(p.virtual_memory().available/(pow(1024, 2)))
        usage = int((p.virtual_memory().total-p.virtual_memory().available)/(pow(1024, 2)))
        available_pr = float(available*100/total)
        usage_pr = float(usage*100/total)
        available_pr = float("{:.2f}".format(available_pr))
        usage_pr = float("{:.2f}".format(usage_pr))
        return ram_tuple(total, available, usage, available_pr, usage_pr)._asdict()
    @classmethod
    def get_memory_info(cls):
        sd_tuple = namedtuple("sd", "total free used free_pr used_pr")
        st = os.statvfs("/home")
        total = int(st.f_blocks*st.f_frsize/(pow(1024, 2)))
        free = int(st.f_bavail*st.f_frsize/(pow(1024, 2)))
        used = int((st.f_blocks-st.f_bfree)*st.f_frsize/(pow(1024, 2)))
        free_pr = float(free*100/total)
        used_pr = float(used*100/total)
        free_pr = float("{:.2f}".format(free_pr))
        used_pr = float("{:.2f}".format(used_pr))
        return sd_tuple(total, free, used, free_pr, used_pr)._asdict()
if __name__ == '__main__':
    M = Monitor()
    while True:
        print(M.get_cpu_info())

        print(M.get_ram_info())

        print(M.get_memory_info())
        sleep(2)

    
