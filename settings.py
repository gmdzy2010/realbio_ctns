# -*- coding: utf-8 -*-
"""
This setting file contains all the settings of realbio_CTNS(Reabio Cluster
Temperature Notification System)
"""


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


# The host name list of all nodes of cluster

CLUSTER_HOST = {
    "login_node": [
        "login-0-0",
        "login-0-1",
    ],
    "compute_node": [
        "compute-0-0",
        "compute-0-1",
        "compute-0-2",
        "compute-0-3",
    ],
    "storage_node": [
        "login-0-0",
        "login-0-1",
    ],
}

# The WARN(warning) and DANG(danger) temperature of inlet and exhaust of
# cluster respectively

IN_TEMP_LV1 = 30

IN_TEMP_LV2 = 35

EX_TEMP_LV1 = 45

EX_TEMP_LV2 = 60


# The temperature file path

TEMP_FILE_PATH = ""
