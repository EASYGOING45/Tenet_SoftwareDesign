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

"""
获取问卷列表
"""
def getWjList(info,username):
    response = {'code': 0, 'msg': 'success'}
    if username:
        obj = Wj.objects.filter(username=username).order_by('-id')
        detail=[]
        for item in obj:
            temp={}
            temp['id']=item.id
            temp['title']=item.title
            temp['desc']=item.desc
            temp['status']=item.status
            detail.append(temp)
        response['data']={'detail':detail}

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

"""
获取模板库问卷列表
"""
def getTempWjList(info,username):
    response = {'code': 0, 'msg': 'success'}
    page = info.get('page',1)  # 问卷标题
    if username:
        obj = TempWj.objects.all().order_by('id')
        count=obj.count()
        obj=obj[(page - 1) * 5: (page - 1) * 5 + 5]
        detail=[]
        for item in obj:
            temp={}
            temp['tempid']=item.id
            temp['tempname']=item.title
            temp['username'] = item.username
            # temp['desc']=item.desc
            detail.append(temp)
        response['detail']=detail
        response['count']=count

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

"""
删除问卷
"""
def deleteWj(info,username):
    response = {'code': 0, 'msg': 'success'}
    id = info.get('id')#问卷id
    if username and id:
        try:
            Wj.objects.filter(username=username, id=id).delete()#删除问卷
            obj=Question.objects.filter(wjId=id)#查询所有关联问题
            for item in obj:
                Options.objects.filter(questionId=item.id).delete()#删除问题关联的选项
            obj.delete()#删除问卷所有关联问题

            Submit.objects.filter(wjId=id).delete()#删除该问卷的提交信息
            Answer.objects.filter(wjId=id).delete()#删除该问题的所有回答
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


"""
获取问题列表
"""
def getQuestionList(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')#wjid
    if username:
        res=Wj.objects.filter(id=wjId,username=username)
        if res.exists():#判断该问卷id是否为本人创建
            obj=Question.objects.filter(wjId=wjId)
            detail=[]
            for item in obj:
                temp={}
                temp['title']=item.title
                temp['type']=item.type
                temp['id']=item.id#问题id
                temp['row']=item.row
                temp['must']=item.must
                #获取选项
                temp['options']=[]
                if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                    optionItems = Options.objects.filter(questionId=item.id)
                    for optionItem in optionItems:
                        temp['options'].append({'title': optionItem.title, 'id': optionItem.id})
                temp['radioValue']=-1#接收单选框的值
                temp['checkboxValue'] =[]#接收多选框的值
                temp['textValue']=''#接收输入框的值
                detail.append(temp)
            response['detail']=detail
        else:
            response['code'] = '-6'
            response['msg'] = '权限不足'

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


"""
添加问题/更新问题
当传入quetionId为空时->添加问题 不为空时->更新问题
事务处理：当一次插入选项过多时会浪费时间，增加事务处理可大大加快速度（改进后20个选项3秒插入完成）
"""
# @transaction.atomic 是事务装饰器 用于事务处理 保证数据的完整性
@transaction.atomic
def addQuestion(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')#wjid
    q_title=info.get('title')#题目标题
    q_type=info.get('type')#题目类型
    options=info.get('options')#选项
    row=info.get('row')
    must=info.get('must')
    questionId=info.get('questionId')#问题id 可为空
    if wjId and q_title and q_type and must!=None:
        if q_type in ['radio','checkbox','text']:
            if questionId:#问题id存在 更新问题
                newIds=[]
                for temp in options:
                    newIds.append(temp['id'])#将更新后的选项id记录
                allOptions=Options.objects.filter(questionId=questionId)
                #遍历选项 把不在更新后的选项id中的选项删除
                for option in allOptions:
                    if option.id not in newIds:
                        option.delete()
                #更新问题
                Question.objects.filter(wjId=wjId,id=questionId).update(title=q_title,type=q_type,must=must,row=row)
                #更新选项
                for option in options:
                    if option['id']!=0:#选项为已有的 更新
                        Options.objects.filter(questionId=questionId, id=option['id']).update(title=option['title'])
                    else:#选项为新增的 添加
                        Options.objects.create(questionId=questionId,title=option['title'])
            else:#问题id不存在 添加问题
                # 添加问题
                resObj = Question.objects.create(wjId=wjId, title=q_title, type=q_type, row=row,must=must)
                questionId = resObj.id
                response['id'] = questionId
                # 添加选项
                if q_type == 'radio' or q_type == 'checkbox':  # 单选或者多选
                    print(type(options))
                    if options and type(options) == type([]):
                        for item in options:
                            Options.objects.create(questionId=questionId, title=item['title'])
                            # Options(questionId=questionId,title=item)
                    else:  # 传入选项不能为空
                        response['code'] = '-4'
                        response['msg'] = '操作失败'
        else:
            response['code'] = '-5'
            response['msg'] = '传入参数值有误'
            return response
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

"""
删除问题
"""
@transaction.atomic
def deleteQuestion(info,username):
    response = {'code': 0, 'msg': 'success'}
    questionId=info.get('questionId')
    if questionId and username:
        try:
            s_wjId=Question.objects.get(id=questionId).wjId#该题目所属的问卷id
            s_username=Wj.objects.get(id=s_wjId).username#该题目所属的用户名
            if username==s_username:#该题目是此用户创建的 有权限删除
                Question.objects.filter(id=questionId).delete()#删除问题
                Options.objects.filter(questionId=questionId).delete()#删除关联选项
            else:#该题目不是此用户创建的 无权限删除
                response['code'] = '-6'
                response['msg'] = '权限不足'
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response