#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Lăng Văn Huy (23020745)
Node: Main Skill Executor & Interactive Terminal
"""

import sys
import json
import rclpy
from rclpy.node import Node
from assignments_2.llm_planner import HuyLLMPlanner
from assignments_2.task_validator import PlanValidator
from assignments_2.robot_skills import HuyUR3SkillLibrary
from assignments_2.scene_manager import HuySceneManager

class HuySkillExecutorNode(Node):
    def __init__(self):
        super().__init__('assignments_2_executor_node')
        
        print("\nSinh vien: Lang Van Huy  MSSV: 23020745  (P = 3)")
        print("Zone -> object theo MSSV: {'zone_a': 'yellow_cube', 'zone_b': 'blue_cube', 'zone_c': 'red_cube'}")
        print("Cho Gazebo va MoveIt (move_group)...")
        
        self.scene_mgr = HuySceneManager(self)
        self.scene_mgr.setup_scene()

        self.planner = HuyLLMPlanner()
        self.validator = PlanValidator()
        self.skills = HuyUR3SkillLibrary(self)

        # Đưa robot về home khởi động
        self.skills.move_to_home_pose()
        print("home() ... SUCCESS\n")

    def run_interactive(self):
        sim_state = {
            'holding': None,
            'objects': {'red_cube': 'table', 'blue_cube': 'table', 'yellow_cube': 'table'},
            'zones': {'zone_a': None, 'zone_b': None, 'zone_c': None, 'zone_temp': None}
        }

        while rclpy.ok():
            try:
                user_cmd = input("Command> ")
                if not user_cmd.strip():
                    continue
                if user_cmd.lower() in ['exit', 'quit']:
                    break
                if user_cmd.lower() == 'reset':
                    sim_state = {
                        'holding': None,
                        'objects': {'red_cube': 'table', 'blue_cube': 'table', 'yellow_cube': 'table'},
                        'zones': {'zone_a': None, 'zone_b': None, 'zone_c': None, 'zone_temp': None}
                    }
                    print("[RESET] Đã làm mới trạng thái scene.")
                    continue

                print(f"\nUSER COMMAND:\n{user_cmd}\n")

                plan_data = self.planner.process_command(user_cmd)
                print("LLM PLAN:")
                for step in plan_data.get("plan", []):
                    if step.get("skill") == "place":
                        print(f"place({step.get('object')}, {step.get('zone')})")
                    elif step.get("skill") == "pick":
                        print(f"pick({step.get('object')})")
                    else:
                        print("home()")
                print()

                is_valid, msg = self.validator.verify_plan(plan_data, sim_state)
                print(f"VALIDATOR: {msg}\n")

                if not is_valid:
                    print("TASK REJECTED\n")
                    continue

                print("EXECUTION:")
                success_all = True
                for step in plan_data.get("plan", []):
                    s_name = step.get("skill")
                    if s_name == "home":
                        res = self.skills.move_to_home_pose()
                        print(f"home() .................................... {res}")
                    elif s_name == "pick":
                        obj = step.get("object")
                        res = self.skills.execute_pick_action(obj)
                        print(f"pick({obj}) ............................ {res}")
                        for z_name, z_obj in sim_state['zones'].items():
                            if z_obj == obj:
                                sim_state['zones'][z_name] = None
                        sim_state['holding'] = obj
                        sim_state['objects'][obj] = 'gripper'
                    elif s_name == "place":
                        obj = step.get("object")
                        zone = step.get("zone")
                        res = self.skills.execute_place_action(obj, zone)
                        print(f"place({obj}, {zone}) ................... {res}")
                        sim_state['zones'][zone] = obj
                        sim_state['objects'][obj] = zone
                        sim_state['holding'] = None
                    
                    if res != "SUCCESS":
                        success_all = False
                        break

                if success_all:
                    print("\nTASK SUCCESS\n")
                else:
                    print("\nTASK FAILED\n")

            except KeyboardInterrupt:
                break

def main(args=None):
    rclpy.init(args=args)
    node = HuySkillExecutorNode()
    node.run_interactive()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
