#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Amos"
# Date: 2017/10/17


# 搜索配置
search_config = [

    {'name': 'hostname__contains', 'title': '主机名', 'type': 'input'},
    {'name': 'cabinet_num', 'title': "机柜号", 'type': 'input'},
    {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},

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
        'q': 'hostname',
        'display': True,
        'title': '主机名',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@hostname'}},
        'attr': {'edit': 'true', 'origin': '@hostname', 'name': 'hostname'}
    },
    {
        'q': 'sn',
        'display': True,
        'title': '序列号',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}},
        'attr': {'edit': 'true', 'origin': "@sn", 'name': 'sn'},
    },

    {
        'q': 'os_platform',
        'display': True,
        'title': '系统',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_platform'}},
        'attr': {'edit': 'true', 'origin': '@os_platform', 'name': 'os_platform'},

    },
    {
        'q': 'os_version',
        'display': True,
        'title': '系统版本',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_version'}},

    },
    {
        'q': 'server_status_id',
        'display': True,
        'title': '服务器状态',
        'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
        'attr': {'edit': 'true', 'edit-type': 'select', 'choice-key': 'status_choices',
                 'origin': '@server_status_id', 'name': 'server_status_id'},
    },
    {
        'q': None,
        'display': True,
        'title': '操作',
        'text': {'tpl': ' <a href="/edit/{nid}">编辑</a> | <a href="/del/{uid}">删除</a> ',
                 'kwargs': {'nid': '@id', 'uid': '@id'}},
    },
]
