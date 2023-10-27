from django.contrib import admin
from .models import *

# Register your models here.

# 后台管理界面配置

admin.site.site_header = 'BK问卷系统管理后台'
admin.site.site_title = 'BK蓝鲸问卷系统'

#用户列表注册
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','status')
    # list_editable 设置默认可编辑字段，在列表里就可以编辑
    list_editable = ['status']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('username', 'email')
    # 操作选项列表顶部，设置为False不在顶部显示，默认为True。
    actions_on_top = False
    # 操作选项列表底部，设置为False不在底部显示，默认为False。
    actions_on_bottom = True
    #指定搜索字段
    search_fields = ['username']
    # 右侧栏过滤器，按状态进行筛选
    list_filter = ['status']
    
#问卷列表注册
@admin.register(Wj)
class WjAdmin(admin.ModelAdmin):
    list_display = ('title','username','status')
    # list_editable 设置默认可编辑字段，在列表里就可以编辑
    list_editable = ['status']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('title', 'username')
    # 操作选项列表顶部，设置为False不在顶部显示，默认为True。
    actions_on_top = False
    # 操作选项列表底部，设置为False不在底部显示，默认为False。
    actions_on_bottom = True
    # 指定搜索字段
    search_fields = ['username']
    # 右侧栏过滤器，按状态进行筛选
    list_filter = ['status']