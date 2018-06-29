# -*- coding: utf-8 -*-

import json
import logging
import settings
import top.api


class Notifications:
    """
    The short message(sms) and voice message(tts) notifications
    simple encapsulation of alidayu
    """
    __APPKEY = settings.ALIDAYU_APPKEY
    __SECRET = settings.ALIDAYU_SECRET
    
    def __init__(self, host_name=None, cluster_temp=None):
        self.sms_phone_list = settings.SMS_PHONE_LIST
        self.tts_phone_list = settings.TTS_PHONE_LIST
        self.host_name = host_name
        self.cluster_temp = cluster_temp
        self.logger = logging.basicConfig(
            level=logging.INFO, filename='logs/notifications.info',
            format="[%(asctime)s] | %(name)s: %(levelname)s: %(message)s "
        )
        
    def get_authentications(self):
        return self.__APPKEY, self.__SECRET
        
    def sms_notifications(self):
        in_temp = self.cluster_temp['in_temp']
        ex_temp = self.cluster_temp['ex_temp']
        logging.info(
            "STEP 1: configure alidayu sms system for request: appkey, secret"
        )
        logging.info(
            "STEP 2: get inlet/exhaust temperature: %s/%s" % (in_temp, ex_temp)
        )
        
        request = top.api.AlibabaAliqinFcSmsNumSendRequest()
        request.set_app_info(top.appinfo(self.__APPKEY, self.__SECRET))
        request.sms_type = "normal"
        request.sms_free_sign_name = ""
        request.rec_num = ",".join(self.sms_phone_list)
        request.sms_template_code = ""
        request.sms_param = json.dumps({
            'hostname': self.host_name,
            'in_temp': str(self.cluster_temp['in_temp']),
            'ex_temp': str(self.cluster_temp['ex_temp'])
        })
        try:
            response = request.getResponse()
            logging.info('STEP 3: sms send ok {0}'.format(response))
            logging.info('Sms send ok')
            return 1
        except Exception as e:
            logging.info('Sms send error {0}'.format(e))
            return 0

    def tts_notifications(self):
        in_temp = self.cluster_temp['in_temp']
        ex_temp = self.cluster_temp['ex_temp']
        logging.info(
            "STEP 1: configure alidayu tts system for request: appkey, secret"
        )
        logging.info(
            "STEP 2: get inlet/exhaust temperature: %s/%s" % (in_temp, ex_temp)
        )
        
        request = top.api.AlibabaAliqinFcTtsNumSinglecallRequest()
        request.set_app_info(top.appinfo(self.__APPKEY, self.__SECRET))
        request.called_num = ",".join(self.tts_phone_list)
        
        # TODO: the "called_show_number" need to certify
        request.called_show_num = ""
        request.tts_code = ""
        request.tts_param = json.dumps({
            'hostname': self.host_name,
            'in_temp': str(self.cluster_temp['in_temp']),
            'ex_temp': str(self.cluster_temp['ex_temp'])
        })
        try:
            response = request.getResponse()
            logging.info('STEP 3: tts voice send ok {0}'.format(response))
            logging.info('STEP 3: the \"called_show_number\" need to certify')
            return 1
        except Exception as e:
            logging.info('Tts voice send error {0}'.format(e))
            return 0


if __name__ == '__main__':
    host_name = "login-0-1"
    dict_temp = {"in_temp": 25, "ex_temp": 40}
    notifications = Notifications(host_name=host_name, cluster_temp=dict_temp)
    notifications.sms_notifications()
    notifications.tts_notifications()
