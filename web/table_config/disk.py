#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Amos"
# Date: 2017/10/17


# 搜索配置
search_config = [

    {'name': 'model__contains', 'title': '型号', 'type': 'input'},
    {'name': 'slot', 'title': "插槽位", 'type': 'input'},
    {'name': 'pd_type', 'title': '磁盘类型', 'type': 'input'},

]

# table_config参数：q：根据q对应的字段在数据库中取值，title：每个字段在前端的列表中显示的表头
# text：在前端渲染的标签内容，tpl：模板，占位符，kwargs：格式化的所用到的数据,display:是否在表中显示
# attr：标签属性，edit：是否可编辑
table_config = [
    {
        'q': None,
        'display': True,
        'title': '选择',
        'text': {'tpl': '<input type="checkbox" value="{nid}">', 'kwargs': {'nid': '@id'}},
        'attr': {'nid': '@id'}
    },
    {
        'q': 'id',
        'display': False,
        'title': 'ID',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}}
    },
    {
        'q': 'slot',
        'display': True,
        'title': '槽位',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@slot'}},
        'attr': {}
    },

    {
        'q': 'model',
        'display': True,
        'title': '磁盘型号',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@model'}},
        'attr': {'edit': 'true', 'origin': '@model', 'name': 'model'}
    },
    {
        'q': 'pd_type',
        'display': True,
        'title': '磁盘类型',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@pd_type'}},
        'attr': {'edit': 'true', 'origin': '@pd_type', 'name': 'pd_type'}
    },
    {
        'q': 'capacity',
        'display': True,
        'title': '磁盘容量(GB)',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@capacity'}},
        'attr': {'edit': 'true', 'origin': '@capacity', 'name': 'capacity'}
    },

    {
        'q': None,
        'display': True,
        'title': '操作',
        'text': {'tpl': ' <a href="/edit/{nid}">编辑</a> | <a href="/del/{uid}">删除</a> ',
                 'kwargs': {'nid': '@id', 'uid': '@id'}},
    },
]
