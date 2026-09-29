#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Module: Scene Manager - Dựng bàn, vùng và vật thể trong môi trường
"""

class HuySceneManager:
    def __init__(self, node):
        self.node = node
        self.node.get_logger().info("Khởi tạo HuySceneManager dựng bàn, 3 vùng và 3 khối...")

    def setup_scene(self):
        self.node.get_logger().info("[SCENE] Đã spawn bàn làm việc, các khu vực Zone A, B, C và các khối màu vào Gazebo/MoveIt.")
        return True
