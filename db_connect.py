from influxdb import InfluxDBClient
import json
from monitoring import Monitor
from datetime import datetime
from time import sleep
class DBRpiMonitor:
    def __init__(self, h='localhost', p=8086, un="admin2", up="rpi4admin957", db_name="rpiMonitor"):
        self.client = InfluxDBClient(host=h, port=p, username=un, password=up)
        self.client.switch_database(db_name)
    def send_data(self, tag_dict, field_dict, measurment):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [{
            "measurement": measurment,
            "tags": tag_dict,
            "time": current_time,
            "fields":field_dict
            }]
        print(json_body)
        self.client.write_points(json_body)
    def get_data_cpu(self):
        return self.client.query('SELECT * FROM "cpu"')
    def get_data_ram(self):
        return self.client.query('SELECT * FROM "ram"')
    def get_data_sd(self):
        return self.client.query('SELECT * FROM "sd"')



if __name__ == '__main__':
    D = DBRpiMonitor()
    M = Monitor()
    while True:
        D.send_data({"device":"rpi4"}, dict(M.get_cpu_info()), "cpu")
        D.send_data({"device":"rpi4"}, dict(M.get_ram_info()), "ram")
        D.send_data({"device":"rpi4"}, dict(M.get_memory_info()), "sd")
        sleep(20)
