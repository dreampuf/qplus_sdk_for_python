#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Qplus Python SDK
author: soddyque@gmail.com
date: 2012-05-25

"""

from __future__ import with_statement
import time
import random
import hashlib
import hmac
import urllib
import urllib2
import contextlib
import operator

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json
    
class QPlusAPI(object):
    SERVER_OPEN = "http://openid.qplus.com/cgi-bin/%s"
    SERVER_TPNS = "http://tpns.qq.com/cgi-bin/app_push"
    def __init__(self, appkey=None, secret=None):
        self._appkey = appkey
        self._secret = secret + "&" #Qplus require

    def get_sig(self, query):
        """ 返回请求参数的签名，以self._secret作为初始key，按照hmac(sha1)对query + '&' + secret进行处理
        query : string , query应该包含url请求的方法
          例如: app_get_userinfo&QUERYSTRING
        """
        return hmac.new(self._secret, query, digestmod=hashlib.sha1).hexdigest()

    def request_factory(self, url, data=None):
        """ 请求构造函数, 传入请求名称(非完整部分), 以及该请求需要的数据, 即返回响应"""
        pdict = {
            "app_id": self._appkey,
            "app_ts": int(time.time()),
            "app_nonce": random.randint(10000000, 99999999), #随机八位数
        }
        pdict.update(data)
        #pdata = "&".join([k+"="+urllib.quote(str(v)) for k, v in sorted(pdict.iteritems(), key=lambda item: item[0])])
        pdata = urllib.urlencode(sorted(pdict.iteritems(), key=operator.itemgetter(0)))
        sig = self.get_sig(url + "&" + pdata)
        pdata = pdata + "&sig=" +  sig
        request = urllib2.Request(QPlusAPI.SERVER_OPEN%url, pdata)
        with contextlib.closing(urllib2.urlopen(request)) as f:
            return f.read()

    def check_sig(self, data):
        """ 检测Sig是否有效,请将Qplus首次转入的视图GET参数传入 """
        sig_chk = data.pop("sig", None)
        assert sig_chk is not None, "check_sig data must have sig"
        pdata = urllib.urlencode(sorted(data.iteritems(), key=operator.itemgetter(0)))
        sig = self.get_sig(pdata)
        return sig == sig_chk

    def check_login(self, data):
        """验证是否登录成功
        data : {
            app_openid: XXXXXX,
            app_openkey: XXXXXXXXX,
        }
        """
        return json.loads(self.request_factory("app_verify", data))

    def get_userinfo(self, data):
        """返回用户信息
        data : {
            app_openid: XXXXXX,
            app_openkey: XXXXXXXXX,
            app_userip: XXX.XXX.XXX.XXX,
        }
        """

        return json.loads(self.request_factory("app_get_userinfo", data))

    def send_push(self, data=None):
        """ 推送信息 
        data : {
            QPLUSID: APPID
            INSTANCEID: 0 #目前只为0（Qplus文档建议）
            OPTYPE: 1 #PUSH显示类型，只看到1有定义
            PUSHMSGID: 1 #本次push的消息ID
            APPCUSTOMIZE: "XXX" #app 自定义传递参数
            NUM: 1 #app图标右上角显示数字
            TEXT: "X" #推送提示语
        }
        """
        pdict = {
            "APPID": self._appkey,
            "TIME": int(time.time()),
            "NONCE": random.randint(10000000, 99999999), #随机八位数
        }
        pdict.update(data)
        #Push 方法不需要对传入参数UrlEncode
        pdata = "&".join([k+"="+str(v) for k, v in sorted(pdict.iteritems(), key=lambda item: item[0])])
        sig = self.get_sig("app_push&" + pdata)
        pdata = pdata + "&IDENTIFYSTRING=" +  sig
        request = urllib2.Request(QPlusAPI.SERVER_TPNS, pdata)
        with contextlib.closing(urllib2.urlopen(request)) as f:
            return f.read()


###### TestCase #######
import unittest

class QPlusTestCase(unittest.TestCase):
    def setUp(self):
        self.appkey = "" #YOUR app key
        self.secret = "" #YOUR secret
        self.openid = "" #Open Id
        self.openkey = "" #Open key
        self.qa = QPlusAPI(appkey=self.appkey, secret=self.secret)

    def test_check_login(self):
        ret = self.qa.check_login({"app_openid": self.openid, "app_openkey": self.openkey})
        self.assertEqual(ret["valide"], 1)

    def test_userinfo(self):
        ret = self.qa.get_userinfo({
            "app_openid": self.openid,
            "app_openkey": self.openkey,
            "app_userip": "127.0.0.1",
        })
        self.assertTrue(ret["info"] is not None, "Userinfo mustn't be None")

    def test_send_push(self):
        pdata = {
            "QPLUSID": "185832728394E96479E36A199C2C8CBA", #QPlusID Q+的桌面应用ID
            "INSTANCEID": 0, #目前只为0（Qplus文档建议）
            "OPTYPE": 1, #PUSH显示类型，只看到1有定义
            "PUSHMSGID": 1, #本次push的消息ID
            "APPCUSTOMIZE": "XXX", #app 自定义传递参数
            "NUM": 1, #app图标右上角显示数字
            "TEXT": "X", #推送提示语
        }
        ret = self.qa.send_push(pdata)
        self.assertEqual(ret["ERRCODE"], 0) #{"ERRCODE":0,"ERRMSG":"None&#160;errors,&#160;success"}

if __name__ == "__main__":
    unittest.main()
