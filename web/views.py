from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from repository import models
from utils.page import Pagination
from .service import server as server_conf
from .service import disk as disk_conf
import time
import json

# Create your views here.

def server(request):
    return render(request, 'server.html')

def server_json(request):

    service = server_conf.ServerService(request)
    if request.method == 'GET':
        response = service.fetch()
        return JsonResponse(response)

    elif request.method == 'DELETE':

        response = service.delete()
        return JsonResponse(response)

    elif request.method == 'PUT':

        response = service.save()
        return JsonResponse(response)

def disk(request):
    return render(request, 'disk.html')

def disk_json(request):
    service = disk_conf.DiskService(request)
    if request.method == 'GET':
        response = service.fetch()
        return JsonResponse(response)

    elif request.method == 'DELETE':

        response = service.delete()
        return JsonResponse(response)

    elif request.method == 'PUT':

        response = service.save()
        return JsonResponse(response)

def memory(request):
    return render(request, 'memory.html')

def memory_json(request):
    table_config = [
        {
            'q': None,
            'title': '选择',
            'text': {'tpl': '<input type="checkbox" value="{nid}">', 'kwargs': {'nid': '@id'}}
        },
        {
            'q': 'id',
            'title': 'ID',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}}
        },
        {
            'q': 'slot',
            'title': '槽位',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@slot'}}
        },
        {
            'q': 'manufacturer',
            'title': '制造商',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@manufacturer'}}
        },
        {
            'q': 'model',
            'title': '型号',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@model'}}
        },
        {
            'q': 'capacity',
            'title': '容量',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@capacity'}}
        },
        {
            'q': 'sn',
            'title': '内存SN号',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}}
        },
        {
            'q': 'speed',
            'title': '速度',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@speed'}}
        },
        {
            'q': 'server_obj__hostname',
            'title': '服务器',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@server_obj__hostname'}}
        },
        {
            'q': None,
            'title': '操作',
            'text': {'tpl': ' <a href="/edit/{nid}">编辑</a> | <a href="/del/{uid}">删除</a> ',
                     'kwargs': {'nid': '@id', 'uid': '@id'}},
        },
    ]

    values = []

    for item in table_config:
        # q 为真的时候才去数据库中取
        if item['q']:
            values.append(item['q'])

    server_list = models.Memory.objects.values(*values)

    response = {
        'data_list': list(server_list),
        'table_config': table_config
    }

    return JsonResponse(response)

def nic(request):
    return render(request, 'nic.html')

def nic_json(request):
    table_config = [
        {
            'q': None,
            'title': '选择',
            'text': {'tpl': '<input type="checkbox" value="{nid}">', 'kwargs': {'nid': '@id'}}
        },
        {
            'q': 'id',
            'title': 'ID',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}}
        },
        {
            'q': 'name',
            'title': '网卡名称',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@name'}}
        },
        {
            'q': 'hwaddr',
            'title': '网卡mac地址',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@hwaddr'}}
        },
        {
            'q': 'netmask',
            'title': '子网掩码',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@netmask'}}
        },
        {
            'q': 'ipaddrs',
            'title': 'ip地址',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@ipaddrs'}}
        },
        {
            'q': 'server_obj__hostname',
            'title': '服务器',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@server_obj__hostname'}}
        },
        {
            'q': None,
            'title': '操作',
            'text': {'tpl': ' <a href="/edit/{nid}">编辑</a> | <a href="/del/{uid}">删除</a> ',
                     'kwargs': {'nid': '@id', 'uid': '@id'}},
        },
    ]
    values = []

    for item in table_config:
        # q 为真的时候才去数据库中取
        if item['q']:
            values.append(item['q'])

    server_list = models.NIC.objects.values(*values)

    response = {
        'data_list': list(server_list),
        'table_config': table_config
    }

    return JsonResponse(response)

def response_server_list(data_list):
    for row in data_list:
        for item in models.Server.server_status_choices:
            if item[0] == row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
        yield row

def test(request):
    data_list = models.Server.objects.values('hostname','server_status_id')
    return render(request,'test.html',{'server_list':response_server_list(data_list)})