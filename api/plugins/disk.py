#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/29

from repository import models

class Disk(object):
    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.disk_dict = info

    def process(self):
        '''
        处理硬盘数据
        :return: 
        '''
        # 当前服务器新的硬盘集合
        new_disk_info_dict = self.disk_dict['data']
        # 当前服务器旧的硬盘集合
        # old_disk_info_dict = models.Disk.objects.filter(server_obj=server_obj)
        old_disk_info_dict = self.server_obj.disk.all()
        # old_disk = server_obj.disk_set.values('solt', 'model', 'capacity', 'pd_type')

        new_disk_slot_set = set(new_disk_info_dict.keys())
        old_disk_slot_set = {obj.slot for obj in old_disk_info_dict}

        add_slot_list = new_disk_slot_set.difference(old_disk_slot_set)
        del_slot_list = old_disk_slot_set.difference(new_disk_slot_set)
        update_slot_list = old_disk_slot_set.intersection(new_disk_slot_set)

        # 循环创建硬盘信息
        self.add_disk(new_disk_info_dict, add_slot_list)

        # 删除硬盘信息
        self.del_disk(del_slot_list)

        # 循环更新硬盘信息
        self.update_disk(new_disk_info_dict, update_slot_list)

    def add_disk(self, new_disk_info_dict, add_slot_list):
        '''
        添加硬盘
        :param new_disk_info_dict: 最新的硬盘信息
        :param add_slot_list: 需要增加的硬盘槽位列表
        :return: 
        '''
        add_record_list = []
        for slot in add_slot_list:
            value = new_disk_info_dict[slot]
            tmp = '添加硬盘,[%s]服务器,[%s]槽位,[%s]型号,[%s]容量,[%s]类型' % (
                self.server_obj, slot, value.get('model'), value.get('capacity'), value.get('pd_type'))
            add_record_list.append(tmp)
            value['server_obj'] = self.server_obj
            models.Disk.objects.create(**value)
        if add_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(add_record_list))

    def del_disk(self, del_slot_list):
        '''
        删除硬盘
        :param del_slot_list: 需要删除的槽位列表
        :return: 
        '''
        del_record_list = []
        for slot in del_slot_list:
            del_obj = models.Disk.objects.filter(server_obj=self.server_obj, slot=slot).first()
            tmp = '删除硬盘,[%s]服务器,[%s]槽位,[%s]型号,[%s]容量,[%s]类型' % (
            self.server_obj, slot, del_obj.model, del_obj.capacity, del_obj.pd_type)
            del_record_list.append(tmp)

        models.Disk.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()

        if del_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(del_record_list))

    def update_disk(self, new_disk_info_dict, update_slot_list):
        '''
        更新硬盘信息
        :param new_disk_info_dict: 最新的硬盘信息
        :param update_slot_list: 需要更新的硬盘槽位列表
        :return: 
        '''
        update_record_list = []
        for slot in update_slot_list:
            value = new_disk_info_dict[slot]
            disk_obj = models.Disk.objects.filter(server_obj=self.server_obj, slot=slot).first()
            for k, new_val in value.items():
                if k == 'capacity':
                    new_val = float(new_val)
                old_val = getattr(disk_obj, k)
                if old_val != new_val:
                    record = "更新硬盘：[%s]服务器,[%s]插槽,[%s]由[%s]变更为[%s]" % (self.server_obj, slot, k, old_val, new_val)
                    update_record_list.append(record)

                    setattr(disk_obj, k, new_val)
            disk_obj.save()
        if update_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(update_record_list))
