# -*- coding: utf-8 -*-
import json
from pprint import pprint
import codecs
import filecmp


def settings_reader(x):
    """Json parser for settings file"""
    with open('Config/' + x, encoding='utf-8') as data_file:
        read_data = data_file.read()
        data_file.closed
    data = json.loads(read_data)
    return data


def read_authentication():
    """Read Auth Information
    :return: data
    """
    return settings_reader('authentication.json')

def read_config():
    """Read Config Information
    :return: data
    """
    return settings_reader('config.json')

def read_trans(lang):
    """Read Translations
    :return: data
    """
    return settings_reader('Translation/translation.' + lang)




