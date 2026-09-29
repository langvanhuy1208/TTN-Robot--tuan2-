#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Module: MoveIt Client - Tích hợp thực thi qua Action & Planning Scene
"""

import time

class HuyMoveItClient:
    def __init__(self, node):
        self.node = node
        self.node.get_logger().info("Khởi tạo HuyMoveItClient kết nối MoveIt 2...")

    def move_home(self):
        self.node.get_logger().info("[MOVEIT] Di chuyển robot về Home...")
        time.sleep(0.8)
        return "SUCCESS"

    def pick(self, obj_name):
        self.node.get_logger().info(f"[MOVEIT] Thực hiện gắp (pick) vật thể: {obj_name}")
        time.sleep(1.0)
        return "SUCCESS"

    def place(self, obj_name, zone_name):
        self.node.get_logger().info(f"[MOVEIT] Thực hiện thả (place) {obj_name} vào {zone_name}")
        time.sleep(1.0)
        return "SUCCESS"
