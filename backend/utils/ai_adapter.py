import os
import json
import uuid
import asyncio
import threading
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAIAdapter(ABC):
    """
    AI适配器基类，定义统一接口
    """
    
    @abstractmethod
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据原稿数据生成游戏原型
        :param manuscript_data: 原稿数据
        :param params: 生成参数，如style、emotion等
        :return: 生成的游戏原型数据
        """
        pass

class OpenAIAIAdapter(BaseAIAdapter):
    """
    OpenAI适配器实现
    """
    
    def __init__(self):
        # 从环境变量加载API密钥
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            print("警告: OPENAI_API_KEY 环境变量未设置，将使用模拟数据")
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用OpenAI生成游戏原型（模拟实现）
        """
        # 如果没有API密钥，则使用模拟数据
        if not self.api_key:
            print("使用模拟数据生成游戏原型...")
            return self._generate_mock_prototype(manuscript_data, params)
        
        # 这里应该是实际调用OpenAI API的代码
        # 由于我们不能直接调用真实API，这里只展示结构
        print(f"调用OpenAI API生成游戏原型...")
        print(f"原稿数据: {manuscript_data}")
        print(f"参数: {params}")
        
        # 模拟API调用延迟
        time.sleep(5)
        
        # 返回模拟结果
        return self._generate_mock_prototype(manuscript_data, params)
    
    def _generate_mock_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟的游戏原型数据
        """
        # 根据原稿数据生成结构化的游戏数据
        game_name = manuscript_data.get("storyTitle", "未命名游戏")
        emotional_tone = params.get("emotion", "neutral")
        
        # 生成像素风场景
        scenes = self._generate_scenes(manuscript_data, emotional_tone)
        
        # 生成角色体系
        characters = self._generate_characters(manuscript_data, emotional_tone)
        
        # 生成任务流程
        missions = self._generate_missions(manuscript_data)
        
        # 生成互动规则
        interaction_rules = self._generate_interaction_rules()
        
        # 构建游戏原型数据
        prototype_data = {
            "gameId": f"game-{uuid.uuid4().hex[:8]}",
            "gameName": game_name,
            "emotionalTone": emotional_tone,
            "style": params.get("style", "pixel_art"),
            "scenes": scenes,
            "characters": characters,
            "missions": missions,
            "interactionRules": interaction_rules,
            "createdAt": time.time()
        }
        
        return prototype_data
    
    def _generate_scenes(self, manuscript_data: Dict[str, Any], emotional_tone: str) -> list:
        """
        根据原稿生成像素风场景
        """
        # 获取游戏背景
        game_background = manuscript_data.get("gameBackground", "神秘森林")
        
        # 根据背景和情感基调生成场景
        scenes = []
        
        # 默认场景
        default_scenes = [
            {
                "id": "scene_start",
                "name": "起点",
                "backgroundDescription": f"像素风格的{game_background}，充满{emotional_tone}氛围",
                "interactiveElements": [
                    {"type": "npc", "name": "向导", "position": [50, 100], "dialogue": ["欢迎来到这个世界！"]},
                    {"type": "item", "name": "神秘宝箱", "position": [200, 150], "description": "似乎藏着重要物品"}
                ],
                "transitions": [
                    {"targetSceneId": "scene_forest", "condition": "start_game", "description": "进入森林"}
                ]
            },
            {
                "id": "scene_forest",
                "name": "森林",
                "backgroundDescription": "茂密的像素森林，阳光透过树叶洒下斑驳光影",
                "interactiveElements": [
                    {"type": "npc", "name": "精灵", "position": [120, 80], "dialogue": ["小心森林中的危险！"]},
                    {"type": "item", "name": "魔法果实", "position": [250, 200], "description": "据说能恢复体力"}
                ],
                "transitions": [
                    {"targetSceneId": "scene_village", "condition": "find_path", "description": "前往村庄"},
                    {"targetSceneId": "scene_cave", "condition": "explore_deeper", "description": "深入洞穴"}
                ]
            },
            {
                "id": "scene_village",
                "name": "村庄",
                "backgroundDescription": "宁静的像素村庄，房屋错落有致",
                "interactiveElements": [
                    {"type": "npc", "name": "村长", "position": [100, 120], "dialogue": ["旅行者，欢迎来到我们的村庄！"]},
                    {"type": "building", "name": "铁匠铺", "position": [220, 180], "description": "可以购买装备的地方"}
                ],
                "transitions": [
                    {"targetSceneId": "scene_forest", "condition": "leave_village", "description": "回到森林"}
                ]
            }
        ]
        
        # 根据原稿中的任务和角色信息扩展场景
        missions = manuscript_data.get("missions", [])
        characters = manuscript_data.get("characters", [])
        
        # 添加基于任务的场景
        for i, mission in enumerate(missions[:2]):  # 最多添加2个基于任务的场景
            scene = {
                "id": f"scene_mission_{i}",
                "name": f"{mission.get('name', '任务场景')}",
                "backgroundDescription": f"与{mission.get('name', '任务')}相关的场景",
                "interactiveElements": [
                    {
                        "type": "quest_npc", 
                        "name": characters[i % len(characters)].get('name', '任务NPC') if characters else '任务NPC',
                        "position": [100 + i*50, 100 + i*30],
                        "dialogue": [
                            f"你来啦！快帮我{mission.get('name', '完成任务')}吧！",
                            f"任务要求：{mission.get('completionCondition', '未知')}"
                        ]
                    }
                ],
                "transitions": [
                    {
                        "targetSceneId": "scene_start", 
                        "condition": "complete_mission", 
                        "description": "完成任务返回"
                    }
                ]
            }
            default_scenes.append(scene)
        
        return default_scenes
    
    def _generate_characters(self, manuscript_data: Dict[str, Any], emotional_tone: str) -> list:
        """
        根据原稿生成角色体系
        """
        player_character = {
            "id": "player",
            "name": "玩家",
            "appearance": "像素风格的冒险者",
            "personality": "勇敢好奇",
            "initialPosition": "scene_start",
            "dialogues": ["我将探索这个奇妙的世界！"]
        }
        
        characters = [player_character]
        
        # 添加原稿中的角色
        original_characters = manuscript_data.get("characters", [])
        for char_data in original_characters:
            character = {
                "id": f"char_{uuid.uuid4().hex[:6]}",
                "name": char_data.get("name", "未知角色"),
                "appearance": char_data.get("appearance", "像素风角色"),
                "personality": char_data.get("personality", "普通"),
                "initialPosition": "scene_start",  # 默认在起始场景
                "dialogues": [
                    f"你好！我是{char_data.get('name', '角色')}",
                    char_data.get("speechStyle", "普通对话"),
                    f"我们的关系是：{char_data.get('relationships', '朋友')}"
                ]
            }
            characters.append(character)
        
        return characters
    
    def _generate_missions(self, manuscript_data: Dict[str, Any]) -> list:
        """
        根据原稿生成任务流程
        """
        missions = []
        
        original_missions = manuscript_data.get("missions", [])
        for i, orig_mission in enumerate(original_missions):
            mission = {
                "id": f"mission_{i}",
                "name": orig_mission.get("name", f"任务{i+1}"),
                "triggerScene": orig_mission.get("triggerCondition", "scene_start"),
                "completionCondition": orig_mission.get("completionCondition", "与NPC对话"),
                "dialogueContent": orig_mission.get("storyProgression", "完成任务获得奖励"),
                "reward": {"xp": 50, "items": ["金币"]},
                "nextMissionId": f"mission_{i+1}" if i < len(original_missions) - 1 else None
            }
            missions.append(mission)
        
        return missions
    
    def _generate_interaction_rules(self) -> Dict[str, Any]:
        """
        生成互动规则
        """
        return {
            "movement": {
                "up": "向上移动",
                "down": "向下移动", 
                "left": "向左移动",
                "right": "向右移动"
            },
            "dialogueTrigger": {
                "distance": 30,  # 与NPC距离小于30像素时可对话
                "key": "SPACE"   # 按空格键触发对话
            },
            "itemInteraction": {
                "distance": 20,  # 与物品距离小于20像素时可互动
                "key": "E"       # 按E键互动
            }
        }

class WenxinAIAdapter(BaseAIAdapter):
    """
    百度文心一言适配器实现（模拟）
    """
    
    def __init__(self):
        # 从环境变量加载API密钥
        self.api_key = os.environ.get("WENXIN_API_KEY")
        if not self.api_key:
            print("警告: WENXIN_API_KEY 环境变量未设置，将使用模拟数据")
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用文心一言生成游戏原型（模拟实现）
        """
        print(f"调用文心一言API生成游戏原型...")
        print(f"原稿数据: {manuscript_data}")
        print(f"参数: {params}")
        
        # 模拟API调用延迟
        time.sleep(5)
        
        # 使用相同的方法生成模拟数据
        adapter = OpenAIAAdapter()
        return adapter._generate_mock_prototype(manuscript_data, params)

class AIAdapterFactory:
    """
    AI适配器工厂类，用于创建不同类型的AI适配器
    """
    
    @staticmethod
    def create_adapter(adapter_type: str) -> BaseAIAdapter:
        """
        创建指定类型的AI适配器
        :param adapter_type: 适配器类型 ('openai' 或 'wenxin')
        :return: AI适配器实例
        """
        if adapter_type.lower() == 'openai':
            return OpenAIAIAdapter()
        elif adapter_type.lower() == 'wenxin':
            return WenxinAIAdapter()
        else:
            raise ValueError(f"不支持的AI适配器类型: {adapter_type}")

# 全局AI适配器实例
ai_adapter = AIAdapterFactory.create_adapter(os.environ.get("AI_ADAPTER_TYPE", "openai"))