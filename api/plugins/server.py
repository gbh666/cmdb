#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/29
from repository import models
from datetime import datetime

class Server(object):

    def __init__(self,server_obj,basic_dict,board_dict):
        self.server_obj = server_obj
        self.basic_dict = basic_dict
        self.board_dict = board_dict

    def process(self):

        # 更新服务器
        # 把主板的信息和基本信息合到一起
        if not self.basic_dict['status']:
            models.ErrorLog.objects.create(title='数据采集错误',content=self.basic_dict['error_msg'])
            raise ValueError('服务器信息未采集')
        temp = {}
        temp.update(self.basic_dict['data'])
        temp.update(self.board_dict['data'])

        temp.pop('hostname')
        record_list = []

        for k, new_val in temp.items():
            old_val = getattr(self.server_obj, k)
            if old_val != new_val:
                record = "[%s]的[%s]由[%s]变更为[%s]" % (self.server_obj.hostname, k, old_val, new_val)
                record_list.append(record)
                setattr(old_val, k, new_val)
        self.server_obj.latest_date = datetime.now()

        self.server_obj.save()
        if record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(record_list))
