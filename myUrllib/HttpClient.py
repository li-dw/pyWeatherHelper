# -*- coding: utf8 -*-
import httplib
import ssl
import urllib
import urllib2
import sys
import json
import socket
from time import sleep
import requests
from collections import OrderedDict
import logging.handlers
from agency.agency_tools import proxy
reload(sys)
sys.setdefaultencoding('UTF8')

ssl._create_default_https_context = ssl._create_unverified_context
_logger = logging.getLogger("daily")

def get(url):
    try:
        request = urllib2.Request(url=url)
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header('X-Requested-With', 'xmlHttpRequest')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        # request.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
        request.add_header('Accept', '*/*')
        result = urllib2.urlopen(request).read()
        assert isinstance(result, object)
        return result
    except httplib.error as e:
        print e
        pass
    except urllib2.URLError as e:
        print e
        pass
    except urllib2.HTTPBasicAuthHandler, urllib2.HTTPError:
        pass


def Post(url, data):
    try:
        request = urllib2.Request(url=url, data=urllib.urlencode(data))
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0')
        # request = urllib2Post.Request(ajax_url, urllib.urlencode(dc))
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header('X-Requested-With', 'xmlHttpRequest')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        # request.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
        request.add_header('Accept', '*/*')
        # request.add_header('Accept-Encoding', 'gzip, deflate')
        result = urllib2.urlopen(request).read()
        return result
    except httplib.error as e:
        return e
    except urllib2.URLError as e:
        return e
    except urllib2.HTTPBasicAuthHandler, urllib2.HTTPError:
        return ('error')


def _set_header_default():
    header_dict = OrderedDict()
    # header_dict["Accept"] = "application/json, text/plain, */*"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    header_dict[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) 12306-electron/1.0.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    return header_dict

class WX_HTTPClient(object):

    def __init__(self, is_proxy):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.initS()
        self._cdn = None
        self._proxies = None
        if is_proxy is 1:
            self.proxy = proxy()
            self._proxies = self.proxy.setProxy()
            # print(u"设置当前代理ip为 {}, 请注意代理ip是否可用！！！！！请注意代理ip是否可用！！！！！请注意代理ip是否可用！！！！！".format(self._proxies))

    def initS(self):
        self._s = requests.Session()
        self._s.headers.update(_set_header_default())
        return self

    def set_cookies(self, **kwargs):
        """
        设置cookies
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self._s.cookies.set(k, v)

    def get_cookies(self):
        """
        获取cookies
        :return:
        """
        return self._s.cookies.values()

    def del_cookies(self):
        """
        删除所有的key
        :return:
        """
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        """
        删除指定key的session
        :return:
        """
        self._s.cookies.set(key, None)

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def resetHeaders(self):
        self._s.headers.clear()
        self._s.headers.update(_set_header_default())

    def getHeadersHost(self):
        return self._s.headers["Host"]

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def getHeadersReferer(self):
        return self._s.headers["Referer"]

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self

    @property
    def cdn(self):
        return self._cdn

    @cdn.setter
    def cdn(self, cdn):
        self._cdn = cdn

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        is_logger = urls.get("is_logger", False)
        req_url = urls.get("req_url", "")
        re_try = urls.get("re_try", 0)
        s_time = urls.get("s_time", 0)
        is_cdn = urls.get("is_cdn", False)
        is_test_cdn = urls.get("is_test_cdn", False)
        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        if data:
            method = "post"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        self.setHeadersReferer(urls["Referer"])
        if is_logger:
            _logger.log(
                u"url: {0}\n入参: {1}\n请求方式: {2}\n".format(req_url, data, method, ))
        self.setHeadersHost(urls["Host"])
        if is_test_cdn:
            url_host = self._cdn
        elif is_cdn:
            if self._cdn:
                # print(u"当前请求cdn为{}".format(self._cdn))
                url_host = self._cdn
            else:
                url_host = urls["Host"]
        else:
            url_host = urls["Host"]
        for i in range(re_try):
            try:
                # sleep(urls["s_time"]) if "s_time" in urls else sleep(0.001)
                sleep(s_time)
                try:
                    requests.packages.urllib3.disable_warnings()
                except:
                    pass
                response = self._s.request(method=method,
                                           timeout=2,
                                           proxies=self._proxies,
                                           url="https://" + url_host + req_url,
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 200 or response.status_code == 302:
                    if urls.get("not_decode", False):
                        return response.content
                    if response.content:
                        if is_logger:
                            _logger.log(
                                u"出参：{0}".format(response.content))
                        if urls["is_json"]:
                            return json.loads(response.content.decode() if isinstance(response.content, bytes) else response.content)
                        else:
                            return response.content.decode("utf8", "ignore") if isinstance(response.content, bytes) else response.content
                    else:
                        _logger.log(
                            u"url: {} 返回参数为空".format(urls["req_url"]))
                        return error_data
                else:
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
        return error_data
