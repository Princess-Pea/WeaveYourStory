"""
预览功能测试脚本
用于测试像素风游戏预览功能的各个组件
"""

import json
import requests

def test_preview_functions():
    """
    测试预览功能
    """
    print("=== 开始测试像素风游戏预览功能 ===")
    
    base_url = "http://localhost:7860/api/v1"
    headers = {"Authorization": "Bearer test_token"}  # 这里需要有效的token
    
    # 测试获取游戏预览数据
    print("\n1. 测试获取游戏预览数据...")
    try:
        game_id = "test_game"  # 使用测试游戏ID
        preview_response = requests.get(
            f"{base_url}/game/preview/{game_id}",
            headers=headers
        )
        
        if preview_response.status_code == 200:
            preview_result = preview_response.json()
            print(f"   预览数据获取成功! 游戏名称: {preview_result.get('data', {}).get('gameName', 'Unknown')}")
            print(f"   场景数量: {len(preview_result.get('data', {}).get('scenes', []))}")
        else:
            print(f"   预览数据获取失败: {preview_response.status_code}, {preview_response.text}")
            # 尝试使用默认游戏ID
            default_response = requests.get(
                f"{base_url}/game/preview/default",
                headers=headers
            )
            if default_response.status_code == 200:
                print("   使用默认游戏ID成功获取数据")
            else:
                print("   即使使用默认ID也无法获取数据")
    except Exception as e:
        print(f"   预览数据请求出错: {str(e)}")
    
    # 测试获取像素素材
    print("\n2. 测试获取像素素材...")
    try:
        asset_response = requests.get(
            f"{base_url}/asset/pixel",
            headers=headers
        )
        
        if asset_response.status_code == 200:
            asset_result = asset_response.json()
            print(f"   素材获取成功! 角色类型: {len(asset_result.get('data', {}).get('characters', []))}")
            print(f"   物品类型: {len(asset_result.get('data', {}).get('objects', []))}")
            print(f"   背景类型: {len(asset_result.get('data', {}).get('backgrounds', []))}")
        else:
            print(f"   素材获取失败: {asset_response.status_code}, {asset_response.text}")
    except Exception as e:
        print(f"   素材请求出错: {str(e)}")
    
    # 测试游戏数据结构
    print("\n3. 测试游戏数据结构...")
    try:
        # 使用之前测试保存的数据
        save_payload = {
            "gameId": "test_preview_game",
            "gameData": {
                "gameId": "test_preview_game",
                "gameName": "预览测试游戏",
                "emotionalTone": "治愈",
                "style": "像素风",
                "scenes": [
                    {
                        "id": "scene_preview_1",
                        "name": "测试场景1",
                        "backgroundDescription": "像素风格的测试场景",
                        "interactiveElements": [
                            {
                                "type": "npc",
                                "name": "测试NPC",
                                "position": [100, 100],
                                "dialogue": [
                                    "你好，欢迎来到测试场景！",
                                    "这里可以测试各种功能。"
                                ],
                                "description": "一个测试用的NPC"
                            },
                            {
                                "type": "item",
                                "name": "测试物品",
                                "position": [200, 150],
                                "description": "一个测试用的物品"
                            }
                        ],
                        "transitions": [
                            {
                                "targetSceneId": "scene_preview_2",
                                "condition": "edge_right",
                                "description": "前往场景2"
                            }
                        ]
                    },
                    {
                        "id": "scene_preview_2",
                        "name": "测试场景2",
                        "backgroundDescription": "另一个像素风格的测试场景",
                        "interactiveElements": [
                            {
                                "type": "npc",
                                "name": "第二个NPC",
                                "position": [150, 120],
                                "dialogue": [
                                    "你来到了第二个场景！",
                                    "这里的功能也可以测试。"
                                ],
                                "description": "场景2的NPC"
                            }
                        ],
                        "transitions": [
                            {
                                "targetSceneId": "scene_preview_1",
                                "condition": "edge_left",
                                "description": "返回场景1"
                            }
                        ]
                    }
                ],
                "characters": [
                    {
                        "id": "player_test",
                        "name": "测试玩家",
                        "appearance": "像素风冒险者",
                        "personality": "好奇",
                        "initialPosition": "scene_preview_1",
                        "dialogues": [
                            "我要开始测试了！",
                            "这个预览功能很棒！"
                        ]
                    }
                ],
                "missions": [
                    {
                        "id": "mission_test_1",
                        "name": "测试任务1",
                        "triggerScene": "scene_preview_1",
                        "triggerCondition": "与测试NPC对话",
                        "completionCondition": "了解测试功能",
                        "dialogueContent": "欢迎来到测试环节！",
                        "reward": {"xp": 10, "items": ["测试徽章"]},
                        "nextMissionId": None
                    }
                ]
            }
        }
        
        # 保存测试数据
        save_response = requests.post(
            f"{base_url}/game/save",
            json=save_payload,
            headers=headers
        )
        
        if save_response.status_code == 200:
            print("   测试游戏数据保存成功!")
            
            # 尝试获取刚保存的数据
            test_get_response = requests.get(
                f"{base_url}/game/preview/test_preview_game",
                headers=headers
            )
            
            if test_get_response.status_code == 200:
                test_data = test_get_response.json()
                print(f"   验证获取成功! 场景数量: {len(test_data.get('data', {}).get('scenes', []))}")
            else:
                print(f"   验证获取失败: {test_get_response.status_code}")
        else:
            print(f"   测试数据保存失败: {save_response.status_code}, {save_response.text}")
    except Exception as e:
        print(f"   游戏数据结构测试出错: {str(e)}")
    
    print("\n=== 预览功能测试完成 ===")
    print("\n预览测试步骤说明:")
    print("1. 使用编辑后的游戏数据加载预览页面")
    print("2. 测试角色移动（方向键或点击移动）")
    print("3. 测试NPC对话（接近或点击NPC）")
    print("4. 测试场景跳转（移动到场景边界）")
    print("5. 测试任务提示（触发任务节点）")
    print("6. 使用控制按钮（暂停/重置/返回编辑）")

if __name__ == "__main__":
    test_preview_functions()