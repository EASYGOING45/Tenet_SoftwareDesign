"""
回答问卷请求接口->回答问卷后台处理函数
"""
from django.shortcuts import HttpResponse
import json
from ExamSystem.models import *
from django.db import transaction
import datetime