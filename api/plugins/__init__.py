#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/29

import importlib
from django.conf import settings
from repository import models
from .server import Server

class PluginManager(object):

    def __init__(self):
        self.plugin_items = settings.PLUGIN_ITEMS
        self.basic_key = "basic"
        self.board_key = "board"

    def exec(self,server_dict):
        '''
        :param server_dict: 
        :return: 1.执行完全成功；2.局部失败；3.执行失败；4.服务器不存在
        '''
        ret = {'code':1,'msg':None}

        hostname = server_dict[self.basic_key]['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        # 因为服务器在购入时就已经录入，汇报时更新就可以，不用增加
        if not server_obj:
            ret['code'] = 4
            return ret

        obj = Server(server_obj,server_dict[self.basic_key],server_dict[self.board_key])
        obj.process()

        # 对比更新,适用于[硬盘，网卡，内存，可插拔的插件]
        for k,v in self.plugin_items.items():
            try:
                md_path,cls_name = v.rsplit('.',maxsplit=1)
                md = importlib.import_module(md_path)
                cls = getattr(md,cls_name)
                obj = cls(server_obj,server_dict[k])
                obj.process()
            except Exception as e:   # 如果在这个循环中报错，表示某个部分出错
                ret['code'] = 2

        return ret
