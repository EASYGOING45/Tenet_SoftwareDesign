from django.shortcuts import HttpResponse
import json
from ExamSystem.models import *
from django.db import transaction,connection
from django.db.models import Q
from . import handle
from io import BytesIO
import base64

"""
问卷设计者操作主入口
涉及Opera和loginCheck两个函数
"""
def opera(request):  # 问卷设计者操作主入口
    response={'code':0,'msg':'success'}
    if request.method=='POST': # 如果是post请求
        body=str(request.body,encoding='utf-8') # 获取请求体
        print(body)
        try:
            info = json.loads(body)#解析json报文
        except:
            response['code'] = '-2'
            response['msg'] = '请求格式有误'
        else:
            opera_type = info.get('opera_type')  # 获取操作类型
            username = request.session.get('username')
            if opera_type:#如果操作类型不为空
                if opera_type == 'login':
                    response = login(info, request)
                elif opera_type == 'logincheck':
                    response = loginCheck(request)
                elif opera_type == 'register':
                    response = register(info)
                elif opera_type == 'resetpass':
                    response = resetpass(info)
                elif username:#需要验证username的方法
                    if opera_type == 'add_wj':  # 添加问卷
                        response = addWj(info,username)
                    elif opera_type == 'get_wj_list':  # 获取问卷列表
                        response = getWjList(info,username)
                    elif opera_type == 'get_temp_wj_list':  # 获取问卷列表
                        response = getTempWjList(info,username)
                    elif opera_type == 'delete_wj':  # 删除问卷
                        response = deleteWj(info,username)
                    elif opera_type == 'get_question_list':  # 获取问题列表
                        response = getQuestionList(info,username)
                    elif opera_type == 'add_question':  # 添加问题
                        response = addQuestion(info,username)
                    elif opera_type == 'delete_question':  # 删除问题
                        response = deleteQuestion(info,username)
                    elif opera_type == 'push_wj':  # 发布问卷（更改问卷状态）
                        response = pushWj(info,username)
                    elif opera_type == 'dataAnalysis':#获取统计数据
                        response = dataAnalysis(info)
                    elif opera_type == 'add_temp':#添加模板
                        response = addTemp(info,username)
                    elif opera_type == 'use_temp':#添加模板
                        response = useTemp(info,username)
                    elif opera_type == 'exit':
                        response = exit(request)
                    elif opera_type=='get_text_answer_detail':
                        response=getTextAnswerDetail(info)
                    elif opera_type=='analysis_export_excel':
                        response=analysisExportExcel(info)
                    elif opera_type=='answer_text_to_excel':
                        response=answerText2Excel(info)
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

def loginCheck(request):
    response = {'code': 0,'msg':'success'}
    # 查询django_session 中是否有username，查询失败则抛出异常
    # 查询成功后判断username是否为空 若为空 则返回404错误 不为空 则返回成功信息
    try:
        username = request.session.get('username')
    except:
        response['code'] = '-4'
        response['msg'] = 'session查询失败'
    else:
        if username:
            response['data']={'user':username}
        else:
            response['code']='404'
            response['msg']='未登录'
    return response


"""
添加问卷/更新问卷
当传入id(问卷的id)为空时->添加问卷  不为空时->更新问卷
"""
def addWj(info,username):
    response = {'code':0,'msg':'success'}
    title = info.get('title') # 问卷标题
    desc = info.get('desc') # 问卷描述
    id = info.get('id') # 问卷id 可为空
    if username and title:
        try:
            if id:#id不为空 更新问卷
                res=Wj.objects.get(username=username,id=id)
                res.title=title
                res.desc=desc
                res.save()
            else:#否则 添加问卷
                res = Wj.objects.create(username=username, title=title,desc=desc, status=0)
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
        else:
            if res.id > 0:
                response['id'] = res.id
            else:
                response['code'] = '-4'
                response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response