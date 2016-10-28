#!/usr/bin/env python3

import os
import sys
from abc import ABC, abstractmethod

import conf
import json
import requests
from time import sleep, time
from multiprocessing import Pool
from importlib.machinery import SourceFileLoader


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


class AbstractSensor(ABC):
    """
    A template for the Sensor class
    """
    def __init__(self, sensor_id, name=""):
        self.id = sensor_id
        self.name = name

    @abstractmethod
    def callback(self):
        return 0


class Message(object):
    """
    A message from a sensor
    """
    hive_id = conf.HIVE_ID
    data = []

    def __init__(self, data):
        self.timestamp = time()
        self.data = data


def discover_sensors():
    """
    Loading every sensors' conf
    And check them
    :return:
    """
    import sensor_enabled
    return sensor_enabled.sensor_list


def loop(sensorsObject):
    """
    Code for the loop which is called everytime
    :param sensorsObject:
    :return:
    """
    # Loading the new pool
    # pool = Pool()

    result_list = []

    for captor in sensorsObject:
        result_list.append(logCaptor(captor))
    # pool.apply_async(logCaptor, args = (captor,), callback = result_list.append)
    # pool.close()
    # pool.join()

    # Create the payload to send
    payload = create_message(result_list)

    # TODO : Start a thread for sending the request
    send_message(conf.UPSTREAM_URL, conf.UPSTREAM_PORT, conf.UPSTREAM_PATH, payload)


if __name__ == "__main__":

    sensorsObject = discover_sensors()

    # Launching every thread
    while "Loic est beau":
        loop(sensorsObject)
        sleep(conf.PAUSE_DELAY)
