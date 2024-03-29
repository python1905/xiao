from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.utils.crypto import random

from xiaomi.settings import SMSCONFIG


def send_sms(phone, templateParam):
    client = AcsClient(SMSCONFIG['ACCESS_KEY_ID'], SMSCONFIG['ACCESS_KEY_SECRET'], 'default')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', SMSCONFIG['SignName'])
    request.add_query_param('TemplateCode', SMSCONFIG['TemplateCode'])
    request.add_query_param('TemplateParam', templateParam)

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))

if __name__ == "__main__":
    a = str()
    for i in range(5):
        num = str(random.randint(0, 9))
        a = a + num
    print(a)
    send_sms('13754834137', {'code': a})
