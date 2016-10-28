#!/usr/bin/env python3

import conf
import requests
from time import sleep, time


#############
# Functions #
#############


def logCaptor(captor):
    return captor.getId(), captor.callback()


def create_message(result_list):
    return {'idHive': conf.HIVE_ID, 'timeStamp': time(), 'captorDatas': result_list}


def send_message(host, port, url, payload):
    r = requests.post(host + ':' + str(port) + '/' + url, json=payload)
    return r


class Message(object):
    """
    A message from a sensor
    """
    hive_id = conf.HIVE_ID
    data = []

    def __init__(self, data):
        self.timestamp = time()
        self.data = data


def loop(sensors):
    """
    Code for the loop which is called everytime
    :param sensors:
    :return:
    """
    # Loading the new pool
    # pool = Pool()

    result_list = []

    for captor in sensors:
        result_list.append(logCaptor(captor))
    # pool.apply_async(logCaptor, args = (captor,), callback = result_list.append)
    # pool.close()
    # pool.join()

    # Create the payload to send
    payload = create_message(result_list)

    # TODO : Start a thread for sending the request
    send_message(conf.UPSTREAM_URL, conf.UPSTREAM_PORT, conf.UPSTREAM_PATH, payload)


if __name__ == "__main__":

    sensorsObject = conf.SENSORS

    # Launching every thread
    while "Loic est beau":
        loop(sensorsObject)
        sleep(conf.PAUSE_DELAY)
