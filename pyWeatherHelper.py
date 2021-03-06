#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Entry """

import logging
import logging.config
import logging.handlers
import getWeather
import encodeMessage
import time
import datetime
import  Config.conf as conf
from Config.conf import _get_yaml
from Config.UnicodeFilter import Code
from Config.pushbearConf import sendPushBear
__author__ = 'lidwt'
_logger = logging.getLogger("daily")
def loop():
    try:
        weather_conf = _get_yaml()["Weather"]
        city_num = len(weather_conf["city_name"])
        for data in weather_conf["city_name"]:
            city_name = data
            w = getWeather.Weather(city_name).main()
            # print(w['weather'][0]['date'])
            # print(w['lifestyle'][1]['txt'])
            # log.info("获取天气信息成功!")
            m = encodeMessage.Message(w)
            m.main()
            msg = m.getMessage()
            info = ""
            # print(info)
            for data in msg:
                # print(data)
                info += data
                info += "\n"
            # print(info)
            sendPushBear(info)
            # log.info(m.getMessage())
    except Exception, e:
        _logger.exception(e)
    finally:
        time.sleep(1)
def run():
    i = 1
    Code()
    exe_hours = _get_yaml()["set"]["exe_hours"]
    # print(exe_hours)
    _logger.info(u"run程序开始运行!")
    while True:
        now = datetime.datetime.now()
        if now.hour in exe_hours and now.minute == 0 :
            _logger.info(u"时间到{}，开始loop".format(now))
            loop()
            i += 1
            _logger.info(u"程序休眠中...")
            time.sleep(60)#确保一分钟内值执行一次
        _logger.info(u"时间未到{}".format(now))
        # 不到时间就等3秒之后再次检测
        time.sleep(3)

if __name__ == '__main__':
    print("Run")
    run()