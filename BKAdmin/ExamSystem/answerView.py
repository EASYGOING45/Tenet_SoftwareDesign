"""
回答问卷请求接口->回答问卷后台处理函数
"""
from django.shortcuts import HttpResponse
import json
from ExamSystem.models import *
from django.db import transaction
import datetime

"""
问卷回答接口 主入口
"""
def opera(request):
    response={'code':0,'msg':'success'}
    if request.method=='POST':
        body=str(request.body,encoding='utf-8')
        print(body)
        try:
            info = json.loads(body)#解析json报文
        except:
            response['code'] = '-2'
            response['msg'] = '请求格式有误'
        opera_type=info.get('opera_type')#获取操作类型
        if opera_type:
            if opera_type=='get_info':#获取问卷信息
                response=getInfo(info,request)
            elif opera_type=='get_temp_info':#获取问卷信息
                response=getTempInfo(info,request)
            elif opera_type=='submit_wj':#提交问卷
                response=submitWj(info,request)
            else:
                response['code'] = '-7'
                response['msg'] = '请求类型有误'
        else:
            response['code'] = '-3'
            response['msg'] = '确少必要参数'
    else:
        response['code']='-1'
        response['msg']='请求方式有误'

    return HttpResponse(json.dumps(response))