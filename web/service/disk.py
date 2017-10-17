#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Amos"
# Date: 2017/10/17
from ..table_config import disk as server_conf
from repository import models
from utils.page import Pagination
from .base import BaseService
import json

class DiskService(BaseService):

    def __init__(self,request):
        self.request = request
        self.table_config = server_conf.table_config
        self.search_config = server_conf.search_config

    def fetch(self):
        # 获取用户请求页码
        current_page = self.request.GET.get('pageNum')
        total_item_count = models.Disk.objects.filter(self.condition()).count()
        page_obj = Pagination(current_page, total_item_count, per_page_count=2)
        server_list = models.Disk.objects.filter(self.condition()).values(*self.values())[page_obj.start:page_obj.end]

        # 把配置信息和在数据库中取到的值json后返回给前端
        response = {
            'search_config': self.search_config,
            'data_list': list(server_list),
            'table_config': self.table_config,
            'global_choices_dict': {

            },
            'page_html': page_obj.page_html_js()
        }
        return response

    def delete(self):

        id_list = json.loads(self.request.body, encoding="utf-8")

        response = {
            'status': True,
            'msg': None
        }

        try:
            models.Disk.objects.filter(id__in=id_list).delete()
        except Exception as e:
            response['status'] = False
            response['msg'] = e

        return response

    def save(self):
        response = {
            'status': True,
            'msg': None
        }

        server_list = json.loads(self.request.body)
        print(server_list)
        for item in server_list:
            nid = item.pop('nid')
            try:
                models.Disk.objects.filter(id=nid).update(**item)
            except Exception as e:
                response['status'] = False
                response['msg'] = e

        return response