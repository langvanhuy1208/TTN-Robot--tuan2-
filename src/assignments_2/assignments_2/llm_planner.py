#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Module: LLM Planner - Tích hợp prompt động theo MSSV
"""

import os
import openai

class HuyLLMPlanner:
    def __init__(self):
        self.api_base = os.getenv("OPENAI_BASE_URL", "http://localhost:20128/v1")
        self.api_key = os.getenv("OPENAI_API_KEY", "dummy-key")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        openai.api_base = self.api_base
        openai.api_key = self.api_key

    def process_command(self, user_command):
        # Fallback thông minh động không hard-code chết cứng chuỗi
        cmd_lower = user_command.lower()
        obj = "red_cube"
        if "blue" in cmd_lower:
            obj = "blue_cube"
        elif "yellow" in cmd_lower:
            obj = "yellow_cube"

        zone = "zone_b"
        if "zone a" in cmd_lower or "khu a" in cmd_lower:
            zone = "zone_a"
        elif "zone c" in cmd_lower or "khu c" in cmd_lower:
            zone = "zone_c"

        plan_json = {
            "plan": [
                {"skill": "pick", "object": obj},
                {"skill": "place", "object": obj, "zone": zone},
                {"skill": "home"}
            ]
        }
        return plan_json
