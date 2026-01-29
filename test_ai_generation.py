"""
AI生成测试脚本
用于测试提交原稿→AI生成→查询状态的全流程
"""

import json
import time
import requests

def test_ai_generation_flow():
    """
    测试AI生成的完整流程
    """
    print("=== 开始测试AI生成流程 ===")
    
    # 模拟的原稿数据
    manuscript_data = {
        "storyTitle": "像素小镇的奇幻冒险",
        "emotionalTone": "治愈",
        "storyOutline": "在一个美丽的像素小镇，主人公需要寻找失踪的朋友，途中会遇到各种有趣的NPC和挑战。",
        "gameBackground": "像素风格的田园小镇，有森林、河流和古老的城堡",
        "missions": [
            {
                "name": "寻找失踪的朋友",
                "triggerCondition": "与村长对话",
                "completionCondition": "找到朋友并带回村子",
                "storyProgression": "解锁新的地图区域"
            },
            {
                "name": "收集魔法水晶",
                "triggerCondition": "完成第一个任务",
                "completionCondition": "收集齐3颗水晶",
                "storyProgression": "获得进入古老城堡的钥匙"
            }
        ],
        "characters": [
            {
                "name": "艾米",
                "personality": "温柔善良",
                "appearance": "短发女孩，穿着蓝色连衣裙",
                "speechStyle": "温和亲切",
                "relationships": "主人公的好友，后来失踪了"
            },
            {
                "name": "老爷爷",
                "personality": "智慧慈祥",
                "appearance": "白胡子老人，戴着圆框眼镜",
                "speechStyle": "充满哲理",
                "relationships": "小镇的智者，会给主人公指引"
            }
        ]
    }
    
    print("1. 准备测试数据...")
    payload = {
        "content": json.dumps(manuscript_data, ensure_ascii=False),
        "context": {"gameId": "test"},
        "params": {
            "style": "像素风",
            "emotion": "治愈"
        }
    }
    
    print("2. 提交AI生成任务...")
    # 注意：这里需要根据实际情况调整API地址
    try:
        response = requests.post(
            "http://localhost:7860/api/v1/ai/game/submit",
            json=payload,
            headers={"Authorization": "Bearer test_token"}  # 这里需要有效的token
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   任务提交成功! taskId: {result.get('data', {}).get('taskId')}")
            task_id = result.get('data', {}).get('taskId')
            
            if task_id:
                print("3. 开始轮询任务状态...")
                status_check_count = 0
                max_checks = 20  # 最多检查20次
                
                while status_check_count < max_checks:
                    time.sleep(3)  # 等待3秒后查询
                    status_response = requests.get(
                        f"http://localhost:7860/api/v1/ai/task/{task_id}",
                        headers={"Authorization": "Bearer test_token"}
                    )
                    
                    if status_response.status_code == 200:
                        status_result = status_response.json()
                        task_status = status_result.get('data', {}).get('status', 'unknown')
                        progress = status_result.get('data', {}).get('progress', 0)
                        
                        print(f"   状态: {task_status}, 进度: {progress}%")
                        
                        if task_status == 'completed':
                            print("   任务完成!")
                            print(f"   生成的游戏数据预览: {json.dumps(status_result.get('data', {}).get('result', {})[:100] if isinstance(status_result.get('data', {}).get('result', {}), str) else status_result.get('data', {}).get('result', {}), indent=2)[:200]}...")
                            break
                        elif task_status == 'failed':
                            print(f"   任务失败: {status_result.get('data', {}).get('errorMsg', '未知错误')}")
                            break
                    else:
                        print(f"   查询状态失败: {status_response.status_code}")
                    
                    status_check_count += 1
                    
                    if status_check_count >= max_checks:
                        print("   超时，停止查询")
            else:
                print("   未能获取到任务ID")
        else:
            print(f"   任务提交失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"   请求出错: {str(e)}")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_ai_generation_flow()