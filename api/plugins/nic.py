#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/29
from repository import models


class Nic(object):
    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.nic_dict = info

    def process(self):
        '''
        处理网卡数据
        :return: 
        '''
        new_nic_info_dict = self.nic_dict['data']

        old_nic_info_list = self.server_obj.nic.all()

        new_disk_name_set = set(new_nic_info_dict.keys())
        old_disk_name_set = {obj.name for obj in old_nic_info_list}

        add_name_list = new_disk_name_set.difference(old_disk_name_set)
        del_name_list = old_disk_name_set.difference(new_disk_name_set)
        update_name_list = old_disk_name_set.intersection(new_disk_name_set)

        # 循环创建信息
        self.add_nic(add_name_list,new_nic_info_dict)

        # 循环删除信息
        self.del_nic(del_name_list)

        # 循环更新信息
        self.update_nic(update_name_list,new_nic_info_dict)

    def add_nic(self,add_name_list,new_nic_info_dict):
        '''
        添加网卡信息
        :param add_name_list: 需要添加的网卡name
        :param new_nic_info_dict: 最新的网卡信息
        :return: 
        '''

        add_record_list = []
        for name in add_name_list:
            value = new_nic_info_dict[name]
            value['name'] = name
            value['server_obj'] = self.server_obj
            tmp = '添加网卡,[%s]服务器,网卡名称[%s],mac地址[%s],子网掩码[%s],ip[%s]' % (
                self.server_obj,name, value.get('hwaddr'), value.get('netmask'), value.get('ipaddrs'))
            add_record_list.append(tmp)
            models.NIC.objects.create(**value)
        if add_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(add_record_list))


    def del_nic(self,del_name_list):
        '''
        删除网卡信息
        :param del_name_list: 需要删除的网卡name
        :return: 
        '''
        del_record_list = []
        for name in del_name_list:
            del_obj = models.NIC.objects.filter(server_obj=self.server_obj, name=name).first()
            tmp = '删除硬盘,[%s]服务器,网卡名称[%s],mac地址[%s],子网掩码[%s],ip[%s]' % (
                self.server_obj,name, del_obj.hwaddr, del_obj.netmask, del_obj.ipaddrs)
            del_record_list.append(tmp)

        models.NIC.objects.filter(server_obj=self.server_obj, name__in=del_name_list).delete()
        if del_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(del_record_list))

    def update_nic(self,update_name_list,new_nic_info_dict):
        '''
        更新网卡信息
        :param update_name_list: 可能更新的网卡列表
        :param new_nic_info_dict: 最新的网卡信息
        :return: 
        '''

        update_record_list = []  #服务器网卡更新记录列表
        for name in update_name_list:
            value = new_nic_info_dict[name]
            nic_obj = models.NIC.objects.filter(server_obj=self.server_obj, name=name).first()
            for k, new_val in value.items():
                old_val = getattr(nic_obj, k) #用反射的方法取到旧的值
                if old_val != new_val:
                    record = "更新网卡：[%s]服务器,网卡名字：[%s],[%s]由[%s]变更为[%s]" % (self.server_obj, name, k, old_val, new_val)
                    update_record_list.append(record)
                    setattr(nic_obj, k, new_val)
            nic_obj.save()
        if update_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(update_record_list))
