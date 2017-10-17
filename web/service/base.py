#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Amos"
# Date: 2017/10/17
import json

class BaseService(object):

    def values(self):
        # 循环配置信息，拿到需要取值的字段
        values = []
        for item in self.table_config:
            # q 为真的时候才去数据库中取
            if item['q']:
                values.append(item['q'])
        return values

    def condition(self):
        # 获取搜索条件
        condition_dict = json.loads(self.request.GET.get('condition'))
        """
        {
            server_status_id: [1,2],
            hostname: ['c1.com','c2.com']
        }
        """
        from django.db.models import Q
        con = Q()
        for k, v in condition_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item,))
            con.add(temp, 'AND')
        return con
