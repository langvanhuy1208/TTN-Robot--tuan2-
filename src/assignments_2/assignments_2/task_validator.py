#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Module: Task Validator - Kiểm tra logic trạng thái, chống khóa lạ, giải phóng zone khi pick
"""

ALLOWED_OBJECTS = ["red_cube", "blue_cube", "yellow_cube"]
ALLOWED_ZONES = ["zone_a", "zone_b", "zone_c", "zone_temp"]
ALLOWED_SKILLS = ["home", "pick", "place"]

class PlanValidator:
    @staticmethod
    def verify_plan(plan_data, state=None):
        if not isinstance(plan_data, dict) or "plan" not in plan_data:
            return False, "Lỗi: Kế hoạch thiếu khóa bắt buộc 'plan'."

        steps = plan_data.get("plan", [])
        if not isinstance(steps, list) or len(steps) == 0:
            return False, "Lỗi: Danh sách plan rỗng."

        if len(steps) > 20:
            return False, f"Lỗi: Kế hoạch quá dài ({len(steps)} bước), tối đa 20 bước."

        if state is None:
            sim_state = {
                'holding': None,
                'objects': {obj: 'table' for obj in ALLOWED_OBJECTS},
                'zones': {zone: None for zone in ALLOWED_ZONES}
            }
        else:
            sim_state = {
                'holding': state.get('holding'),
                'objects': dict(state.get('objects', {obj: 'table' for obj in ALLOWED_OBJECTS})),
                'zones': dict(state.get('zones', {zone: None for zone in ALLOWED_ZONES}))
            }

        allowed_keys_per_skill = {
            "home": ["skill"],
            "pick": ["skill", "object"],
            "place": ["skill", "object", "zone"]
        }

        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                return False, f"Lỗi: Bước số {idx+1} không phải object hợp lệ."
            
            skill = step.get("skill")
            if skill not in ALLOWED_SKILLS:
                return False, f"Lỗi bước {idx+1}: skill khong hop le: {skill}"

            step_keys = list(step.keys())
            allowed_keys = allowed_keys_per_skill.get(skill, [])
            invalid_keys = [k for k in step_keys if k not in allowed_keys]
            if invalid_keys:
                return False, f"Lỗi bước {idx+1}: khoa khong cho phep: {invalid_keys}"

            if skill == "pick":
                obj = step.get("object")
                if obj not in ALLOWED_OBJECTS:
                    return False, f"Lỗi bước {idx+1}: object khong hop le: {obj}"
                
                if sim_state['holding'] is not None:
                    return False, f"Lỗi bước {idx+1}: Không thể pick khi đang cầm vật '{sim_state['holding']}'."
                
                for z_name, z_obj in sim_state['zones'].items():
                    if z_obj == obj:
                        sim_state['zones'][z_name] = None
                
                sim_state['holding'] = obj
                sim_state['objects'][obj] = 'gripper'

            elif skill == "place":
                obj = step.get("object")
                zone = step.get("zone")

                if obj not in ALLOWED_OBJECTS:
                    return False, f"Lỗi bước {idx+1}: object khong hop le: {obj}"
                if zone not in ALLOWED_ZONES:
                    return False, f"Lỗi bước {idx+1}: zone khong hop le: {zone}"

                if sim_state['holding'] is None:
                    return False, f"Lỗi bước {idx+1}: chua pick {obj} (đang không cầm vật nào)."
                
                if sim_state['holding'] != obj:
                    return False, f"Lỗi bước {idx+1}: Đang cầm vật '{sim_state['holding']}' nhưng lại yêu cầu place vật '{obj}'."

                if sim_state['zones'].get(zone) is not None and zone != 'zone_temp':
                    return False, f"Lỗi bước {idx+1}: Khu vực đích '{zone}' đang bị chiếm!"

                sim_state['zones'][zone] = obj
                sim_state['objects'][obj] = zone
                sim_state['holding'] = None

            elif skill == "home":
                pass

        if sim_state['holding'] is not None:
            return False, f"Lỗi: Kết thúc kế hoạch nhưng robot vẫn đang cầm vật '{sim_state['holding']}'."

        return True, "Kế hoạch hợp lệ hoàn toàn."
