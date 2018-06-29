import argparse
from conf import settings
from core.host_temperature import HostTemperature
from core.notifications import Notifications


def get_argument():
    parser = argparse.ArgumentParser(description="To get the arguments")
    parser.add_argument('-s', '--ensure_sms', dest='ensure_sms', default=True,
                        action='store_true', help='To ensure the sms alert')
    parser.add_argument('-t', '--ensure_tts', dest='ensure_tts', default=False,
                        action='store_true', help='To ensure the tts alert')
    parser.add_argument('-d', '--ensure_deb', dest='ensure_deb', default=False,
                        action='store_true', help='Enable debug logging info')
    parser.add_argument('-v', '--version', action='version', version="1.0.0")
    return parser.parse_args()


def get_specified_host(host_kind="compute_node", ensure_sms=True,
                       ensure_tts=False):
    for host in settings.CLUSTER_HOST[host_kind]:
        host_temp = HostTemperature(
            host, logs_file_path=settings.LOGS_FILE_PATH,
            temp_file_path=settings.TEMP_FILE_PATH,
        )
        cluster_temp = host_temp.get_host_temperature()
        in_temp, ex_temp = cluster_temp["in_temp"], cluster_temp["ex_temp"]
        notifications = Notifications(
            host, cluster_temp=cluster_temp,
            appkey=settings.ALIDAYU_APPKEY, secret=settings.ALIDAYU_SECRET,
            logs_file_path=settings.LOGS_FILE_PATH,
        )
        if settings.IN_TEMP_LV2 <= in_temp or settings.EX_TEMP_LV2 <= ex_temp:
            if ensure_sms:
                notifications.sms_notifications(
                    sms_phone_list=",".join(settings.SMS_PHONE_LIST)
                )
            if ensure_tts:
                notifications.tts_notifications(
                    tts_phone_list=",".join(settings.TTS_PHONE_LIST)
                )
            notifications.email_notifications(
                email_host=settings.EMAIL_HOST,
                username=settings.EMAIL_USERNAME,
                password=settings.EMAIL_PASSWORD,
                email_receiver_list=settings.EMAIL_RECEIVER_LIST,
            )
            return "ALERT-LV2"
        if settings.IN_TEMP_LV1 <= in_temp or settings.EX_TEMP_LV1 <= ex_temp:
            if ensure_sms:
                notifications.sms_notifications(
                    sms_phone_list=",".join(settings.SMS_PHONE_LIST)
                )
            notifications.email_notifications(
                email_host=settings.EMAIL_HOST,
                username=settings.EMAIL_USERNAME,
                password=settings.EMAIL_PASSWORD,
                email_receiver_list=settings.EMAIL_RECEIVER_LIST,
            )
            return "ALERT-LV1"


def run(enable_compute=True, enable_login=False, enable_storage=True,
        ensure_sms=True, ensure_tts=False):
    if enable_login:
        get_specified_host(host_kind="login_node", ensure_sms=ensure_sms,
                           ensure_tts=ensure_tts)
    if enable_compute:
        get_specified_host(host_kind="compute_node", ensure_sms=ensure_sms,
                           ensure_tts=ensure_tts)
    if enable_storage:
        get_specified_host(host_kind="storage_node", ensure_sms=ensure_sms,
                           ensure_tts=ensure_tts)


if __name__ == "__main__":
    # argument = get_argument()
    # ensure_sms = argument.ensure_sms
    # ensure_tts = argument.ensure_tts
    # run(enable_login=True, enable_compute=False, enable_storage=False,
    #     ensure_tts=ensure_tts, ensure_sms=ensure_sms)
    run(ensure_sms=False)
