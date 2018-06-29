import json
import logging
import os
import smtplib
import top.api
from email.mime.text import MIMEText
from email.header import Header



class Notifications:
    """
    The short message(sms) and voice message(tts) notifications
    simple encapsulation of alidayu
    """
    def __init__(self, host_name, cluster_temp, appkey=None, secret=None,
                 logs_file_path=None):
        self._appkey, self._secret = appkey, secret
        self.host_name = host_name
        self.cluster_temp = cluster_temp
        self.logs_file_path = logs_file_path
        self.logger = self.set_logger()
    
    def set_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        logger_file = os.path.join(self.logs_file_path, 'notifications.info')
        logger_handler = logging.FileHandler(logger_file)
        logger_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)
        return logger

    def reset_authentications(self, appkey=None, secret=None):
        self._appkey, self._secret = appkey, secret
        return self._appkey, self._secret
    
    def sms_notifications(self, sms_phone_list):
        in_temp = self.cluster_temp['in_temp']
        ex_temp = self.cluster_temp['ex_temp']
        self.logger.info(
            "STEP 1: configure alidayu sms system for request: appkey, secret"
        )
        self.logger.info(
            "STEP 2: get inlet/exhaust temperature: %s/%s" % (in_temp, ex_temp)
        )
        
        request = top.api.AlibabaAliqinFcSmsNumSendRequest()
        request.set_app_info(top.appinfo(self._appkey, self._secret))
        request.sms_type = "normal"
        request.sms_free_sign_name = "锐翌集群"
        request.rec_num = sms_phone_list
        request.sms_template_code = "SMS_10845500"
        request.sms_param = json.dumps({
            'hostname': self.host_name,
            'in_temp': str(in_temp),
            'ex_temp': str(ex_temp)
        })
        try:
            response = request.getResponse()
            self.logger.info('STEP 3: sms send ok {0}'.format(response))
            self.logger.info('Sms send ok')
            return 1
        except Exception as e:
            self.logger.info('Sms send error {0}'.format(e))
            return 0
    
    def tts_notifications(self, tts_phone_list):
        in_temp = self.cluster_temp['in_temp']
        ex_temp = self.cluster_temp['ex_temp']
        self.logger.info(
            "STEP 1: configure alidayu tts system for request: appkey, secret"
        )
        self.logger.info(
            "STEP 2: get inlet/exhaust temperature: %s/%s" % (in_temp, ex_temp)
        )
        
        request = top.api.AlibabaAliqinFcTtsNumSinglecallRequest()
        request.set_app_info(top.appinfo(self._appkey, self._secret))
        request.called_num = tts_phone_list
        
        # TODO: the "called_show_number" need to certify
        request.called_show_num = "051482043271"
        request.tts_code = "TTS_10970049"
        request.tts_param = json.dumps({
            'hostname': self.host_name,
            'in_temp': str(in_temp),
            'ex_temp': str(ex_temp)
        })
        try:
            response = request.getResponse()
            self.logger.info('STEP 3: tts voice send ok {0}'.format(response))
            self.logger.info('STEP 3: the called_show_number need to certify')
            return 1
        except Exception as e:
            self.logger.info('Tts voice send error {0}'.format(e))
            return 0
    
    def email_notifications(self, email_host="smtp.mxhichina.com",
                            username=None, password=None,
                            email_receiver_list=None):
        email_host = email_host
        sender, receivers = username, email_receiver_list
        in_temp = self.cluster_temp['in_temp']
        ex_temp = self.cluster_temp['ex_temp']
        email_content = "节点%s高温警报，进气口温度：%s，出气口温度：%s" % (
            self.host_name, str(in_temp), str(ex_temp)
        )
        message = MIMEText(email_content, "plain", "utf-8")
        message['From'] = Header(sender, 'utf-8')
        message['To'] = Header("admin group", 'utf-8')
        message['Subject'] = Header("集群高温预警", 'utf-8')
        try:
            smtp_obj = smtplib.SMTP(host=email_host, port=80)
            smtp_obj.login(username, password)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            self.logger.info("Email notifications send success!")
        except smtplib.SMTPException as error:
            self.logger.info("Email notifications send fail: %s" % error)
