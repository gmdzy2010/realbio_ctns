import logging
import os
import re
import settings


class HostTemperature:
    """
    To get the inlet/exhaust temperature of each host of the cluster
    """
    def __init__(self, host_name):
        self.host_name = host_name
        self.temp_file_path = settings.TEMP_FILE_PATH
        self.file_exist = True
        self.file_readable = True
        self._in_temp = 0
        self._ex_temp = 0
        self.logger = logging.basicConfig(
            level=logging.INFO, filename='logs/get_temperature.info',
            format="[%(asctime)s] | %(name)s: %(levelname)s: %(message)s "
        )
    
    def _get_temp(self, line):
        if re.search(r'^FP|Inlet', line):
            self._in_temp = line.split(',')[1] if line.split(',')[1] else 0
        elif re.search(r'^MB|Exhaust', line):
            self._ex_temp = line.split(',')[1] if line.split(',')[1] else 0
        return self._in_temp, self._ex_temp
    
    def is_file_exist(self, file_name):
        if not os.access(file_name, os.F_OK):
            logging.info("host log file doesn't exist!")
            self.file_exist = False
        return self.file_exist
    
    def is_file_readable(self, file_name):
        if not os.access(file_name, os.R_OK):
            logging.info("host log file isn't accessible to read!")
            self.file_readable = False
        return self.file_readable
    
    def get_host_temperature(self):
        cluster_temp = {"in_temp": self._in_temp, "ex_temp": self._ex_temp}
        host_file = os.path.join(self.temp_file_path, self.host_name)
        if self.is_file_exist(host_file) and self.is_file_readable(host_file):
            with open(host_file, "r") as fh:
                for line in fh:
                    cluster_temp["in_temp"] = int(self._get_temp(line)[0])
                    cluster_temp["ex_temp"] = int(self._get_temp(line)[1])
            in_temp, ex_temp = cluster_temp["in_temp"], cluster_temp["ex_temp"]
            logging.info(
                " %s: IN/EX %s/%s" % (self.host_name, in_temp, ex_temp)
            )
        else:
            logging.info("Fail to get the temperature of the host")
        return cluster_temp


if __name__ == '__main__':
    host_temp = HostTemperature("login-0-1")
    host_temp.get_host_temperature()
