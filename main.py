#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Entry """

import logging
import logging.config
import logging.handlers
import pyWeatherHelper
import encodeMessage
import  Config.conf as conf
from Config.conf import _get_yaml


__author__ = 'lidwt'

def main_program():
    logging.config.dictConfig(conf.log_setting)
    log = logging.getLogger("daily")
    log.info(u"main程序开始运行!")
    try:
        pyWeatherHelper.run()
    except Exception,e:
        log.info(u"程序运行出错!")
        log.error(e)
    finally:
        log.info(u"程序停止运行!")

if __name__ == '__main__':
    main_program()