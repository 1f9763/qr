#-*- coding:utf-8 -*-
# from django.http import HttpResponse
# import qrcode
# from cStringIO import StringIO
# import  urllib
#
# import hashlib
# import json
# from lxml import etree
# from django.utils.encoding import smart_str
# from django.views.decorators.csrf import csrf_exempt
#
# #
# #
# # def generate_qrcode(request, data):
# #     img = qrcode.make(urllib.unquote(data))
# #
# #     buf = StringIO()
# #     img.save(buf)
# #     image_stream = buf.getvalue()
# #
# #     response = HttpResponse(image_stream, content_type="image/png")
# #     response['Last-Modified'] = 'Mon, 27 Apr 2015 02:05:03 GMT'
# #     response['Cache-Control'] = 'max-age=31536000'
# #     return response
#
#
# WEIXIN_TOKEN = 'pang'
#
# @csrf_exempt
# def index(request):
#     """
#     所有的消息都会先进入这个函数进行处理，函数包含两个功能，
#     微信接入验证是GET方法，
#     微信正常的收发消息是用POST方法。
#     """
#     if request.method == "GET":
#         signature = request.GET.get("signature", None)
#         timestamp = request.GET.get("timestamp", None)
#         nonce = request.GET.get("nonce", None)
#         echostr = request.GET.get("echostr", None)
#         token = WEIXIN_TOKEN
#         tmp_list = [token, timestamp, nonce]
#         tmp_list.sort()
#         tmp_str = "%s%s%s" % tuple(tmp_list)
#         tmp_str = hashlib.sha1(tmp_str).hexdigest()
#         if tmp_str == signature:
#             return HttpResponse(echostr)
#         else:
#             return HttpResponse("weixin  index")
#     else:
#         xml_str = smart_str(request.body)
#         request_xml = etree.fromstring(xml_str)
#         response_xml = auto_reply_main(request_xml)# 修改这里
#         return HttpResponse('nimeia 这是个笑话')
#
# def auto_reply_main():
#     return 'nimeia 这是个笑话'

from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
import  urllib,re#,Skype4Py


WECHAT_TOKEN = 'pang'
AppID = 'wx64c17707fa74457b'
AppSecret = '785fb19d1f90bef88b7570988cec16fc'

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

def helloqt():

    #url='http://news.iciba.com/dailysentence/detail-1479.html'
    url='http://www.azquotes.com/'
    returnHtml=urllib.urlopen(url).read()
    # print blogHtml
    pattern=re.compile('<a class="title.*?">(.*?)</a>.*?<a href=.*?">(.*?)</a>',re.S)
    result=re.findall(pattern,returnHtml)
    result=result[0][0]+'--by '+result[0][1]+'\n <a href="http://helloqt.duapp.com/">post by dakara\'s qt robot</a>'

    return result
    # skype=Skype4Py.Skype()
    # skype.Attach()
    # print 'name',skype.CurrentUser.MoodText
    # skype.CurrentUserProfile._SetMoodText(result)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('本立而道生')
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")


    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()

    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content = (
            '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天'
            '\n【<a href="http://www.xxx.com">dakara qt 微信版</a>】'
            ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '功能':
            reply_text = (
                    '目前支持的功能：\n1. 【qt】两个字可以得到一句哲理，\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '【<a href="http://helloqt.duapp.com/">dakara qt 微信版</a>】'
            )
        elif content.endswith('qt'):
            reply_text = helloqt()

        response = wechat_instance.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")
