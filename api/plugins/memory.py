#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/29

from repository import models

class Memory(object):
    def __init__(self, server_obj, info):
        self.server_obj = server_obj
        self.memory_dict = info

    def process(self):
        '''
        处理内存数据
        :return: 
        '''
        new_memory_info_dict = self.memory_dict['data']
        old_memory_info_list = self.server_obj.memory.all()  # queryset集合，一个个对象

        new_memory_slot_set = set(new_memory_info_dict.keys())

        old_memory_slot_set = {obj.slot for obj in old_memory_info_list}

        add_slot_list = new_memory_slot_set.difference(old_memory_slot_set)
        del_slot_list = old_memory_slot_set.difference(new_memory_slot_set)
        update_slot_list = old_memory_slot_set.intersection(new_memory_slot_set)

        # 循环创建信息
        self.add_memory(add_slot_list,new_memory_info_dict)

        # 循环删除信息
        self.del_memory(del_slot_list)

        # 循环更新信息
        self.update_memory(update_slot_list,new_memory_info_dict)


    def add_memory(self,add_slot_list,new_memory_info_dict):
        '''
        添加内存信息
        :param add_slot_list: 需要添加的内存的槽位号列表
        :param new_memory_info_dict: 最新的内存信息
        :return: 
        '''
        add_record_list = []
        for slot in add_slot_list:
            value = new_memory_info_dict[slot]
            tmp = '添加内存,[%s]服务器,[%s]槽位,[%s]制造商,[%s]型号,[%s]容量,sn号[%s],速度[%s]' % (
                self.server_obj,slot, value.get('manufacturer'), value.get('model'), value.get('capacity'), value.get('sn'),
                value.get('speed'))
            add_record_list.append(tmp)
            value['server_obj'] = self.server_obj
            models.Memory.objects.create(**value)
        if add_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(add_record_list))

    def del_memory(self,del_slot_list):
        '''
        删除内存信息
        :param del_slot_list: 需要删除的内存的槽位号
        :return: 
        '''
        del_record_list = []
        for slot in del_slot_list:
            del_obj = models.Memory.objects.filter(server_obj=self.server_obj, slot=slot).first()
            tmp = '删除内存,[%s]服务器,[%s]槽位,[%s]型号,[%s]容量,[%s]sn号' % (
                self.server_obj,slot, del_obj.model, del_obj.capacity, del_obj.sn)
            del_record_list.append(tmp)

        models.Memory.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()

        if del_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(del_record_list))

    def update_memory(self,update_slot_list,new_memory_info_dict):
        '''
        更新内存信息
        :param update_slot_list: 可能需要更的内存的槽位号
        :param new_memory_info_dict: 最新的内存信息
        :return: 
        '''

        update_record_list = []
        for slot in update_slot_list:
            value = new_memory_info_dict[slot]
            memory_obj = models.Memory.objects.filter(server_obj=self.server_obj, slot=slot).first()
            for k, new_val in value.items():
                old_val = getattr(memory_obj, k)
                if old_val != new_val:
                    record = "更新内存：[%s]服务器,[%s]插槽,[%s]由[%s]变更为[%s]" % (self.server_obj, slot, k, old_val, new_val)
                    update_record_list.append(record)
                    setattr(memory_obj, k, new_val)
                    memory_obj.save()
        if update_record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(update_record_list))