# QPlusSDK for python

## 简介

提供对[QPlus平台](http://www.qplus.com/)SDK Python版本的封装。

## 调用方法

### 声明api封装

    appkey = "XXXXXX" #YOUR app key
    secret = "YYYYYY" #YOUR secret
    oppenid = "XXXXXX" #Open Id
    openkey = "XXXXXX" #Open key
    qa = QPlusAPI(appkey=appkey, secret=secret)

### 调用相应接口方法

    ret = qa.check_login({"app_openid": oppenid, "app_openkey": openkey})
    assertEqual(ret["valide"], 1)

### 调用Push方法

    pdata = {
        "QPLUSID": "185832728394E96479E36A199C2C8CBA", #QPlusID Q+的桌面应用ID
        "INSTANCEID": 0, #目前只为0（Qplus文档建议）
        "OPTYPE": 1, #PUSH显示类型，只看到1有定义
        "PUSHMSGID": 1, #本次push的消息ID
        "APPCUSTOMIZE": "XXX", #app 自定义传递参数
        "NUM": 1, #app图标右上角显示数字
        "TEXT": "X", #推送提示语
    }
    ret = qa.send_push(pdata)
    assertEqual(ret["ERRCODE"], 0) #{"ERRCODE":0,"ERRMSG":"None&#160;errors,&#160;success"}

## License

This project is made available under the following terms.(MIT LICENSE)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

