"""
AI辅助功能测试脚本
用于测试AI辅助生成场景、对话和任务的功能
"""

import json
import requests

def test_ai_assist_functions():
    """
    测试AI辅助功能
    """
    print("=== 开始测试AI辅助功能 ===")
    
    base_url = "http://localhost:7860/api/v1"
    headers = {"Authorization": "Bearer test_token"}  # 这里需要有效的token
    
    # 测试AI辅助生成场景
    print("\n1. 测试AI辅助生成场景...")
    try:
        scene_payload = {
            "content": "宁静的村庄，有小溪和树林",
            "context": {
                "sceneName": "村庄",
                "gameId": "test_game"
            },
            "params": {
                "style": "像素风",
                "emotion": "治愈"
            }
        }
        
        scene_response = requests.post(
            f"{base_url}/ai/assist/scene",
            json=scene_payload,
            headers=headers
        )
        
        if scene_response.status_code == 200:
            scene_result = scene_response.json()
            print(f"   场景生成成功! 结果: {scene_result.get('data', {}).get('result', '')[:100]}...")
        else:
            print(f"   场景生成失败: {scene_response.status_code}, {scene_response.text}")
    except Exception as e:
        print(f"   场景生成请求出错: {str(e)}")
    
    # 测试AI辅助生成对话
    print("\n2. 测试AI辅助生成对话...")
    try:
        dialog_payload = {
            "content": "欢迎来到村庄，请问需要帮助吗？",
            "context": {
                "characterName": "村长",
                "gameId": "test_game"
            },
            "params": {
                "style": "像素风",
                "emotion": "温暖"
            }
        }
        
        dialog_response = requests.post(
            f"{base_url}/ai/assist/dialog",
            json=dialog_payload,
            headers=headers
        )
        
        if dialog_response.status_code == 200:
            dialog_result = dialog_response.json()
            print(f"   对话生成成功! 结果: {dialog_result.get('data', {}).get('result', '')[:100]}...")
        else:
            print(f"   对话生成失败: {dialog_response.status_code}, {dialog_response.text}")
    except Exception as e:
        print(f"   对话生成请求出错: {str(e)}")
    
    # 测试AI辅助设计任务
    print("\n3. 测试AI辅助设计任务...")
    try:
        task_payload = {
            "content": "寻找丢失的猫咪",
            "context": {
                "taskName": "找猫咪",
                "gameId": "test_game"
            },
            "params": {
                "style": "像素风",
                "emotion": "治愈"
            }
        }
        
        task_response = requests.post(
            f"{base_url}/ai/assist/task",
            json=task_payload,
            headers=headers
        )
        
        if task_response.status_code == 200:
            task_result = task_response.json()
            print(f"   任务设计成功! 结果: {task_result.get('data', {}).get('result', '')[:100]}...")
        else:
            print(f"   任务设计失败: {task_response.status_code}, {task_response.text}")
    except Exception as e:
        print(f"   任务设计请求出错: {str(e)}")
    
    # 测试游戏数据保存
    print("\n4. 测试游戏数据保存...")
    try:
        save_payload = {
            "gameId": "test_game",
            "gameData": {
                "gameId": "test_game",
                "gameName": "测试游戏",
                "scenes": [
                    {
                        "id": "scene_1",
                        "name": "测试场景",
                        "backgroundDescription": "这是一个测试场景",
                        "interactiveElements": [],
                        "transitions": []
                    }
                ],
                "characters": [
                    {
                        "id": "char_1",
                        "name": "测试角色",
                        "appearance": "测试外观",
                        "personality": "测试性格",
                        "initialPosition": "scene_1",
                        "dialogues": ["测试对话"]
                    }
                ],
                "missions": [
                    {
                        "id": "mission_1",
                        "name": "测试任务",
                        "triggerScene": "scene_1",
                        "triggerCondition": "测试触发条件",
                        "completionCondition": "测试完成条件",
                        "dialogueContent": "测试对话内容",
                        "reward": {"xp": 10, "items": ["测试物品"]},
                        "nextMissionId": None
                    }
                ]
            }
        }
        
        save_response = requests.post(
            f"{base_url}/game/save",
            json=save_payload,
            headers=headers
        )
        
        if save_response.status_code == 200:
            save_result = save_response.json()
            print(f"   游戏保存成功! 状态: {save_result.get('msg', '')}")
        else:
            print(f"   游戏保存失败: {save_response.status_code}, {save_response.text}")
    except Exception as e:
        print(f"   游戏保存请求出错: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_ai_assist_functions()