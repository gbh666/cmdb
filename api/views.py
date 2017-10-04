from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from repository import models
from .plugins import PluginManager
import json
from django.db.models import Q
from datetime import date
import hashlib
import time

# ######################### API验证 #############################
def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()

key = "dhkbckzjgksdagfhjsdafhjgsdfksd"

visited_keys = {
    # "dhkbckzjgksdagfhjsdafhjgsdfksd":时间
}

def api_auth(func):
    def inner(request,*args,**kwargs):
        server_float_ctime = time.time()
        # 在请求头中获取用户传过来的验证字符串
        auth_header_val = request.META['HTTP_AUTH_API']
        client_md5_str,client_ctime = auth_header_val.split("|",1)
        client_float_time = float(client_ctime)

        # 第一关
        if (client_float_time+10) < server_float_ctime:
            return HttpResponse("你走")

        # 第二关
        server_md5_str = md5("%s|%s" %(key,client_ctime,))
        if server_md5_str != client_md5_str:
            return HttpResponse("你走吧")

        # 第三关
        if visited_keys.get(client_md5_str):
            return HttpResponse("你他妈走不走")

        visited_keys[client_md5_str] = client_float_time
        return func(request,*args,**kwargs)
    return inner
# #################################################################

@csrf_exempt
@api_auth
def server(request):
    '''给客户端提供API'''
    if request.method == "GET":
        #获取今日未采集的主机列表
        current_date = date.today()
        host_list = models.Server.objects.filter(
            Q(Q(latest_date=None)|Q(latest_date__date__lt=current_date))&Q(server_status_id=2)
        ).values('hostname') # [0:200] 如果服务器非常多，可以加个切片操作，半小时拿200个
        host_list = list(host_list)
        return HttpResponse(json.dumps(host_list))


    elif request.method == "POST":
        server_dict = json.loads(request.body.decode('utf-8'))
        # 1.检查server表中是否有当前资产信息【主机名是唯一标识】
        if not server_dict['basic']['status']:
            return HttpResponse('爸爸搞不了')
        manager = PluginManager()
        response=manager.exec(server_dict)

        return HttpResponse(json.dumps(response))

@api_auth
def test(request):
    return HttpResponse("正常用户")
















