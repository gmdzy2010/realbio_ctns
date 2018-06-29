import logging
import os
import re


class HostTemperature:
    """
    To get the inlet/exhaust temperature of each host of the cluster
    """
    def __init__(self, host_name, temp_file_path=None, logs_file_path=None):
        self.host_name = host_name
        self.temp_file_path = temp_file_path
        self.file_exist = True
        self.file_readable = True
        self._in_temp = 0
        self._ex_temp = 0
        self.logs_file_path = logs_file_path
        self.logger = self.set_logger()

    def set_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        logger_file = os.path.join(self.logs_file_path, 'get_temperature.info')
        logger_handler = logging.FileHandler(logger_file)
        logger_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)
        return logger

    def _get_temp(self, line):
        if re.search(r'^FP|Inlet', line):
            self._in_temp = line.split(',')[1] if line.split(',')[1] else 0
        elif re.search(r'^MB|Exhaust', line):
            self._ex_temp = line.split(',')[1] if line.split(',')[1] else 0
        return self._in_temp, self._ex_temp
    
    def is_file_exist(self, file_name):
        if not os.access(file_name, os.F_OK):
            self.logger.info("File %s doesn't exist!" % self.host_name)
            self.file_exist = False
        return self.file_exist
    
    def is_file_readable(self, file_name):
        if not os.access(file_name, os.R_OK):
            self.logger.info(
                "File %s isn't accessible to read!" % self.host_name
            )
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
            self.logger.info(
                "%s: IN/EX %s/%s" % (self.host_name, in_temp, ex_temp)
            )
        else:
            self.logger.info(
                "Fail to get the temperature of the %s" % self.host_name
            )
        return cluster_temp


if __name__ == '__main__':
    host_temp = HostTemperature(
        "login-0-1", temp_file_path="", logs_file_path=""
    )
    host_temp.get_host_temperature()