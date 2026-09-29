#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Module: Robot Skills - Thư viện kỹ năng điều khiển chính
"""

from assignments_2.moveit_client import HuyMoveItClient

class HuyUR3SkillLibrary:
    def __init__(self, node):
        self.moveit = HuyMoveItClient(node)
        print("[SKILLS INIT] Thư viện kỹ năng của Lăng Văn Huy (23020745) đã sẵn sàng.")

    def move_to_home_pose(self):
        return self.moveit.move_home()

    def execute_pick_action(self, target_object):
        return self.moveit.pick(target_object)

    def execute_place_action(self, target_object, destination_zone):
        return self.moveit.place(target_object, destination_zone)
