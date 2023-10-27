from django.db import models

# Create your models here.
# 用户信息表
class User(models.Model):
    username = models.CharField(max_length=20,primary_key=True,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    email=models.CharField(max_length=30,verbose_name='邮箱',null=True)  # null=True表示可以为空
    status_type = ((0,u'正常'),(1,u'禁用'))  # u表示unicode编码
    status=models.IntegerField(choices=status_type,verbose_name='状态',default=0) # 0表示正常，1表示禁用
    # Meta类是一个内部类，它用于定义一些Django模型类的行为特性
    class Meta:
        verbose_name = u'用户' # verbose_name表示单数形式 用于admin后台显示
        verbose_name_plural = u'用户列表'  # verbose_name_plural表示复数形式
        
# 问卷概览表
class Wj(models.Model):
    title=models.CharField(max_length=50,verbose_name='问卷标题')
    username = models.CharField(max_length=20,verbose_name='发起人') # 关联用户名
    status_type = ((0,u'未发布'),(1,u'已发布'))
    status=models.IntegerField(choices=status_type,verbose_name='是否发布',default=0)#0未发布 1已发布
    desc=models.TextField(verbose_name='问卷说明',null=True)#问卷描述 在问卷头部展示

    class Meta:
        verbose_name = u'问卷'
        verbose_name_plural = u'问卷列表'
        
    
# 问卷表
class Question(models.Model):
    title = models.CharField(max_length=100,verbose_name='题目标题')
    type = models.CharField(max_length=20,verbose_name='题目类型')
    wjId= models.IntegerField(verbose_name='关联问卷id')
    row = models.IntegerField(verbose_name='行数',null=True) # 如果为填空题，则此字段为文本输入框的行数
    must = models.BooleanField(verbose_name='是否必填')
    
# 问卷选项表
class Options(models.Model):
    questionId = models.IntegerField(verbose_name='关联题目id')
    title = models.CharField(max_length=100,verbose_name='选项名')
    
# 提交信息表
class Submit(models.Model):
    wjId = models.IntegerField(verbose_name = '关联问卷id')
    submitTime=models.DateTimeField(verbose_name='提交时间')
    submitIp = models.CharField(max_length=15,verbose_name='提交IP')
    useTime=models.IntegerField(verbose_name='填写用时') # 单位：秒
    
# 回答表
class Answer(models.Model):
    wjId = models.IntegerField(verbose_name='关联问题id')
    submitId = models.IntegerField(verbose_name='关联提交id')
    wjId = models.IntegerField(verbose_name='问卷id')
    type = models.CharField(max_length=20,verbose_name='题目类型')
    answer = models.IntegerField(verbose_name='答案',blank=True,null=True)
    answerText = models.TextField(verbose_name='文本答案',blank=True,null=True)
    
# 模板库问卷表
class TempWj(models.Model):
    title = models.CharField(max_length=50,verbose_name='问卷标题')
    username = models.CharField(max_length=20,verbose_name='创建人') # 关联用户名
    desc=models.TextField(verbose_name='问卷说明',null=True) # 问卷描述 在问卷头部展示

# 模板库问题表
class TempQuestion(models.Model):
    title=models.CharField(max_length=100,verbose_name='题目标题')
    type=models.CharField(max_length=20,verbose_name='题目类型')
    wjId=models.IntegerField(verbose_name='关联问卷id')
    row=models.IntegerField(verbose_name='行数',null=True)#如果为填空题 此字段为文本输入框的行数
    must=models.BooleanField(verbose_name='是否必填')#是否必填

#模板库选项表
class TempOptions(models.Model):
    questionId = models.IntegerField(verbose_name='关联题目id')
    title=models.CharField(max_length=100,verbose_name='选项名')