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

"""
获取问卷信息
"""
def getInfo(info,request):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')
    username = request.session.get('username')
    if wjId:
        try:#判断问卷id是否存在
            res=Wj.objects.get(id=wjId)#查询id为wjId
            response['title']=res.title
            response['desc']=res.desc
        except:
            response['code'] = '-10'
            response['msg'] = '问卷不存在'
        else:
            if res.username==username or res.status==1:#只有问卷发布者或者此问卷为已发布才能查看
                obj = Question.objects.filter(wjId=wjId)
                detail = []
                for item in obj:
                    temp = {}
                    temp['title'] = item.title
                    temp['type'] = item.type
                    temp['id'] = item.id  # 问题id
                    temp['row'] = item.row
                    temp['must'] = item.must
                    # 获取选项
                    temp['options'] = []
                    if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                        optionItems = Options.objects.filter(questionId=item.id)
                        for optionItem in optionItems:
                            temp['options'].append({'title':optionItem.title,'id':optionItem.id})
                    temp['radioValue'] = -1  # 接收单选框的值
                    temp['checkboxValue'] = []  # 接收多选框的值
                    temp['textValue'] = ''  # 接收输入框的值
                    detail.append(temp)
                response['detail'] = detail
            else:
                response['code'] = '-10'
                response['msg'] = '问卷尚未发布'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response