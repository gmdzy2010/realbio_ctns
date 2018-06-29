"""
This setting file contains all the settings of realbio_CTNS (Reabio Cluster
Temperature Notification System)
Last edit by liy, 06/29/2018, 21:30:23
"""


import os


# Certifications to access ALIDAYU

ALIDAYU_APPKEY = ""

ALIDAYU_SECRET = ""


# Phone numbers to notify when the cluster is overload

SMS_PHONE_LIST = [
    "",
]
TTS_PHONE_LIST = [
    "",
]

EMAIL_RECEIVER_LIST = [
    "",
]


# The host name list of all nodes of cluster

CLUSTER_HOST = {
    "login_node": [
        "login-0-0",
        "login-0-1",
        "login-0-2",
    ],
    "compute_node": [
        "compute-0-0",
        "compute-0-1",
        "compute-0-2",
        "compute-0-3",
    ],
    "storage_node": [
        "nas-0-0",
    ],
}


# The WARN(warning) and DANG(danger) temperature of inlet and exhaust of
# cluster respectively

IN_TEMP_LV1 = 32

IN_TEMP_LV2 = 36

EX_TEMP_LV1 = 60

EX_TEMP_LV2 = 70


# The file path settings

TEMP_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)

LOGS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)


# Email settings

EMAIL_HOST = ""

EMAIL_USERNAME = ""

EMAIL_PASSWORD = ""
