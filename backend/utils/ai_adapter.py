import os
import json
import uuid
import asyncio
import threading
import time
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from functools import wraps


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    重试装饰器，用于API调用失败时自动重试
    :param max_retries: 最大重试次数
    :param delay: 初始延迟时间（秒）
    :param backoff: 延迟递增倍数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"API调用失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}")
                        print(f"将在 {current_delay:.1f} 秒后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"API调用失败，已达到最大重试次数: {e}")
            raise last_exception
        return wrapper
    return decorator


class AIConfig:
    """AI服务配置类"""
    # OpenAI配置
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 百度文心一言配置
    WENXIN_API_KEY = os.environ.get("WENXIN_API_KEY", "")
    WENXIN_SECRET_KEY = os.environ.get("WENXIN_SECRET_KEY", "")
    WENXIN_MODEL = os.environ.get("WENXIN_MODEL", "ernie-bot-4")
    
    # 阿里通义千问配置
    QIANWEN_API_KEY = os.environ.get("QIANWEN_API_KEY", "")
    QIANWEN_MODEL = os.environ.get("QIANWEN_MODEL", "qwen-turbo")
    
    # 魔搭社区配置（使用DashScope API）
    MODELSCOPE_KEY = os.environ.get("MODELSCOPE_KEY", "")
    MODELSCOPE_MODEL = os.environ.get("MODELSCOPE_MODEL", "qwen-turbo")
    
    # 通用配置
    AI_ADAPTER_TYPE = os.environ.get("AI_ADAPTER_TYPE", "modelscope")
    AI_REQUEST_TIMEOUT = int(os.environ.get("AI_REQUEST_TIMEOUT", 60))
    AI_MAX_RETRIES = int(os.environ.get("AI_MAX_RETRIES", 3))


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
    
    @abstractmethod
    def assist_with_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        AI辅助生成场景
        :param content: 现有内容
        :param context: 上下文信息
        :param params: 生成参数
        :return: 生成的场景内容
        """
        pass
    
    @abstractmethod
    def assist_with_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        AI辅助生成对话
        :param content: 现有内容
        :param context: 上下文信息
        :param params: 生成参数
        :return: 生成的对话内容
        """
        pass
    
    @abstractmethod
    def assist_with_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        AI辅助设计任务
        :param content: 现有内容
        :param context: 上下文信息
        :param params: 生成参数
        :return: 生成的任务内容
        """
        pass
    
    @abstractmethod
    def assist_with_manuscript(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        AI辅助补全原稿表单
        :param content: 现有表单内容（JSON字符串）
        :param context: 上下文信息
        :param params: 生成参数
        :return: 补全后的完整表单内容（JSON字符串）
        """
        pass

class OpenAIAIAdapter(BaseAIAdapter):
    """
    OpenAI适配器实现 - 支持真实API调用
    """
    
    def __init__(self):
        self.api_key = AIConfig.OPENAI_API_KEY
        self.api_base = AIConfig.OPENAI_API_BASE
        self.model = AIConfig.OPENAI_MODEL
        self.timeout = AIConfig.AI_REQUEST_TIMEOUT
        if not self.api_key:
            print("警告: OPENAI_API_KEY 环境变量未设置，将使用模拟数据")
    
    def _build_game_prompt(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """构建游戏原型生成提示词 - 增强版"""
        story_title = manuscript_data.get("storyTitle", "未命名游戏")
        game_background = manuscript_data.get("gameBackground", "")
        characters = manuscript_data.get("characters", [])
        missions = manuscript_data.get("missions", [])
        
        return f"""你是一个专业的像素风格叙事冒险游戏设计师，擅长创作情感丰富、逻辑连贯的游戏内容。

## 原稿信息
- 故事标题: {story_title}
- 游戏背景: {game_background}
- 角色数量: {len(characters)}
- 任务数量: {len(missions)}

## 完整原稿数据
{json.dumps(manuscript_data, ensure_ascii=False, indent=2)}

## 生成要求
- 风格: {params.get('style', 'pixel_art')} (像素艺术风格)
- 情感基调: {params.get('emotion', 'neutral')}

## 设计原则
1. **场景连贯性**: 场景之间的过渡要自然，有明确的逻辑关系
2. **角色一致性**: 角色的对话要符合其性格设定，保持人设统一
3. **任务驱动**: 任务要推动故事发展，有明确的前后因果关系
4. **情感表达**: 根据情感基调设计场景氛围和角色互动
5. **像素美学**: 所有视觉描述要符合像素风格特点

## 输出JSON格式
{{
  "scenes": [
    {{
      "id": "scene_xxx",
      "name": "场景名称",
      "backgroundDescription": "像素风场景详细描述",
      "atmosphere": "场景氛围（如：温馨、神秘、紧张）",
      "interactiveElements": [
        {{"type": "npc/item/trigger", "name": "元素名", "position": [x, y], "dialogue": ["对话1"], "description": "描述"}}
      ],
      "transitions": [
        {{"targetSceneId": "scene_xxx", "condition": "触发条件", "description": "过渡描述", "transitionEffect": "过渡效果"}}
      ]
    }}
  ],
  "characters": [
    {{
      "id": "char_xxx",
      "name": "角色名",
      "appearance": "像素风外观描述",
      "personality": "性格特点",
      "role": "角色定位（主角/NPC/反派）",
      "initialPosition": "初始场景ID",
      "dialogues": ["对话内容"],
      "emotionalArcs": ["情感变化描述"]
    }}
  ],
  "missions": [
    {{
      "id": "mission_xxx",
      "name": "任务名",
      "description": "任务详细描述",
      "triggerScene": "触发场景ID",
      "triggerCondition": "触发条件",
      "objectives": ["目标1", "目标2"],
      "completionCondition": "完成条件",
      "reward": {{"xp": 0, "items": [], "unlocks": []}},
      "nextMissionId": "下一任务ID或null",
      "storyProgression": "任务推动的剧情发展"
    }}
  ],
  "interactionRules": {{
    "movement": {{"up": "W", "down": "S", "left": "A", "right": "D"}},
    "dialogueTrigger": {{"distance": 30, "key": "SPACE"}},
    "itemInteraction": {{"distance": 20, "key": "E"}}
  }},
  "narrativeFlow": {{
    "openingScene": "开场场景ID",
    "keyPlotPoints": ["关键剧情点描述"],
    "endings": ["可能的结局"]
  }}
}}

请确保生成的内容逻辑连贯、情感丰富、符合像素风格美学。只返回JSON数据，不要包含其他说明文字。"""

    def _build_scene_prompt(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """构建场景生成提示词 - 增强版"""
        scene_name = context.get('sceneName', '新场景')
        previous_scene = context.get('previousScene', '')
        next_scenes = context.get('nextScenes', [])
        related_characters = context.get('relatedCharacters', [])
        
        return f"""你是一个专业的像素风格游戏场景设计师，擅长创造沉浸式的游戏环境。

## 场景信息
- 场景名称: {scene_name}
- 前置场景: {previous_scene or '无（开场场景）'}
- 后续场景: {', '.join(next_scenes) if next_scenes else '待定'}
- 相关角色: {', '.join(related_characters) if related_characters else '无'}
- 现有内容: {content}

## 设计参数
- 视觉风格: {params.get('style', '像素风')}
- 情感基调: {params.get('emotion', '治愈')}

## 设计要求
1. **像素美学**: 描述要体现像素艺术的特点（有限色彩、清晰轮廓、复古感）
2. **场景过渡**: 与前后场景有逻辑连接，过渡自然
3. **互动设计**: 设计有意义的互动元素，推动剧情或提供探索乐趣
4. **氛围营造**: 通过光影、色调、音效建议营造符合情感基调的氛围

## 请生成以下内容
1. **背景描述**: 详细的像素风场景视觉描述（100字以内）
2. **氛围元素**: 光线、天气、时间等氛围设定
3. **可互动元素**: 至少3个互动点（NPC/物品/机关）
4. **场景跳转**: 与其他场景的连接方式和条件
5. **隐藏要素**: 可选的隐藏内容或彩蛋

请用中文回答，格式清晰，重点突出。"""

    def _build_dialog_prompt(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """构建对话生成提示词 - 增强版"""
        character_name = context.get('characterName', 'NPC')
        personality = context.get('personality', '友善')
        relationship = context.get('relationship', '初次见面')
        story_context = context.get('storyContext', '')
        
        return f"""你是一个专业的游戏对话编剧，擅长创作符合角色性格的生动对话。

## 角色信息
- 角色名称: {character_name}
- 性格特点: {personality}
- 与玩家关系: {relationship}
- 剧情背景: {story_context or '一般交流'}
- 现有内容: {content}

## 设计参数
- 游戏风格: {params.get('style', '像素风')}
- 情感基调: {params.get('emotion', '治愈')}

## 对话设计原则
1. **性格一致**: 对话要完全符合角色性格设定
2. **情感层次**: 根据剧情展现角色的情感变化
3. **信息传递**: 自然地融入剧情线索或任务提示
4. **互动感**: 留有玩家选择或回应的空间
5. **像素风格**: 语言简洁有力，符合复古游戏的文字风格

## 请生成以下内容
1. **开场白**: 角色见到玩家时的第一句话
2. **主要对话**: 3-5句核心对话内容
3. **分支选项**: 可能的玩家回应选项（2-3个）
4. **告别语**: 对话结束时的话语
5. **情感标注**: 每句话的情感状态

请用中文回答，对话要自然流畅，符合角色身份。"""

    def _build_task_prompt(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """构建任务生成提示词 - 增强版"""
        task_name = context.get('taskName', '新任务')
        story_phase = context.get('storyPhase', '中期')
        previous_task = context.get('previousTask', '')
        related_characters = context.get('relatedCharacters', [])
        
        return f"""你是一个专业的游戏任务设计师，擅长设计有趣且推动剧情的游戏任务。

## 任务信息
- 任务名称: {task_name}
- 故事阶段: {story_phase}
- 前置任务: {previous_task or '无（初始任务）'}
- 相关角色: {', '.join(related_characters) if related_characters else '待定'}
- 现有内容: {content}

## 设计参数
- 游戏风格: {params.get('style', '像素风')}
- 情感基调: {params.get('emotion', '治愈')}

## 任务设计原则
1. **剧情推动**: 任务要推动主线剧情发展
2. **难度适中**: 挑战性与趣味性平衡
3. **奖励合理**: 奖励与任务难度匹配
4. **连贯性**: 与前后任务有逻辑关联
5. **情感体验**: 任务过程要传递情感价值

## 请生成以下内容
1. **任务名称**: 简洁有力的任务标题
2. **任务描述**: 详细的任务背景和目标（50字以内）
3. **触发条件**: 如何解锁此任务
4. **任务目标**: 具体的完成步骤（2-4个子目标）
5. **完成条件**: 明确的完成判定
6. **奖励设计**: 经验值、道具、解锁内容
7. **剧情推进**: 完成任务后的剧情发展
8. **后续任务**: 解锁的下一个任务（如有）

请用中文回答，设计要有创意且符合游戏整体风格。"""

    @retry_on_failure(max_retries=AIConfig.AI_MAX_RETRIES)
    def _call_openai_api(self, prompt: str) -> str:
        """调用OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """使用OpenAI生成游戏原型"""
        if not self.api_key:
            print("使用模拟数据生成游戏原型...")
            return self._generate_mock_prototype(manuscript_data, params)
        
        try:
            print(f"调用OpenAI API生成游戏原型...")
            prompt = self._build_game_prompt(manuscript_data, params)
            response = self._call_openai_api(prompt)
            
            # 尝试解析JSON响应
            try:
                game_data = json.loads(response)
                game_data["gameId"] = f"game-{uuid.uuid4().hex[:8]}"
                game_data["gameName"] = manuscript_data.get("storyTitle", "未命名游戏")
                game_data["emotionalTone"] = params.get("emotion", "neutral")
                game_data["style"] = params.get("style", "pixel_art")
                game_data["createdAt"] = time.time()
                return game_data
            except json.JSONDecodeError:
                print("API响应解析失败，使用模拟数据...")
                return self._generate_mock_prototype(manuscript_data, params)
                
        except Exception as e:
            print(f"OpenAI API调用失败: {e}，使用模拟数据...")
            return self._generate_mock_prototype(manuscript_data, params)
    
    def assist_with_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成场景"""
        if not self.api_key:
            return self._generate_mock_scene(content, context, params)
        
        try:
            prompt = self._build_scene_prompt(content, context, params)
            return self._call_openai_api(prompt)
        except Exception as e:
            print(f"场景生成失败: {e}，使用模拟数据...")
            return self._generate_mock_scene(content, context, params)
    
    def assist_with_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成对话"""
        if not self.api_key:
            return self._generate_mock_dialog(content, context, params)
        
        try:
            prompt = self._build_dialog_prompt(content, context, params)
            return self._call_openai_api(prompt)
        except Exception as e:
            print(f"对话生成失败: {e}，使用模拟数据...")
            return self._generate_mock_dialog(content, context, params)
    
    def assist_with_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助设计任务"""
        if not self.api_key:
            return self._generate_mock_task(content, context, params)
        
        try:
            prompt = self._build_task_prompt(content, context, params)
            return self._call_openai_api(prompt)
        except Exception as e:
            print(f"任务生成失败: {e}，使用模拟数据...")
            return self._generate_mock_task(content, context, params)

    def assist_with_manuscript(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助补全原稿表单"""
        if not self.api_key:
            return self._generate_mock_manuscript(content, context, params)
        
        try:
            prompt = self._build_manuscript_prompt(content, context, params)
            return self._call_openai_api(prompt)
        except Exception as e:
            print(f"原稿补全失败: {e}，使用模拟数据...")
            return self._generate_mock_manuscript(content, context, params)

    def _build_manuscript_prompt(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """构建原稿表单补全提示词"""
        try:
            form_data = json.loads(content)
        except:
            form_data = {}
            
        story_title = form_data.get("storyTitle", "")
        story_outline = form_data.get("storyOutline", "")
        
        return f"""你是一个专业的像素风格游戏策划和剧本作家。
请根据用户提供的部分原稿内容（主要是剧情名称和故事大纲），补全剩余的游戏原稿表单。

## 已有内容
- 剧情名称: {story_title}
- 故事大纲: {story_outline}
- 其他已填内容: {json.dumps(form_data, ensure_ascii=False, indent=2)}

## 补全要求
1. **情感基调**: 根据大纲选择合适的情感基调（如：温暖、治愈、神秘、紧张、感伤）。
2. **游戏背景**: 详细描述一个符合大纲的像素风游戏世界背景。
3. **角色设计**: 设计3-4个富有魅力的角色，包括他们的外观（像素风）、性格和对话风格。
4. **任务设计**: 设计3-4个推动剧情的任务，包括触发条件、完成条件和剧情推进。
5. **逻辑连贯**: 补全的内容必须与原有的剧情名称和故事大纲严格保持一致且逻辑自洽。

## 输出格式
请直接返回JSON格式的数据，字段必须与输入的JSON格式完全一致：
{{
  "storyTitle": "...",
  "selectedEmotionOption": "...",
  "emotionalTone": "...",
  "customEmotionalTone": "...",
  "storyOutline": "...",
  "gameBackground": "...",
  "missions": [
    {{ "name": "...", "triggerCondition": "...", "completionCondition": "...", "storyProgression": "..." }}
  ],
  "characters": [
    {{ "name": "...", "appearance": "...", "personality": "...", "speechStyle": "...", "relationships": "..." }}
  ]
}}

只返回JSON对象，不要包含任何多余文字或Markdown格式。"""

    def _generate_mock_manuscript(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """生成模拟的原稿补全内容"""
        try:
            form_data = json.loads(content)
        except:
            form_data = {}
            
        story_title = form_data.get("storyTitle", "未命名剧情")
        story_outline = form_data.get("storyOutline", "暂无大纲")
        
        mock_data = {
            "storyTitle": story_title,
            "selectedEmotionOption": "warm",
            "emotionalTone": "温暖",
            "customEmotionalTone": "",
            "storyOutline": story_outline,
            "gameBackground": f"这是一个基于《{story_title}》的像素风世界，充满了怀旧与冒险的气息。",
            "missions": [
                { "name": "初步探索", "triggerCondition": "进入游戏", "completionCondition": "与第一个NPC对话", "storyProgression": "了解了世界的基本情况" },
                { "name": "寻找线索", "triggerCondition": "完成任务1", "completionCondition": "找到神秘物品", "storyProgression": "发现了隐藏的真相" }
            ],
            "characters": [
                { "name": "主角", "appearance": "身穿蓝衣的像素冒险者", "personality": "热血勇敢", "speechStyle": "直接坦诚", "relationships": "自己" },
                { "name": "老村长", "appearance": "白胡子的矮小像素老者", "personality": "睿智和蔼", "speechStyle": "语重心长", "relationships": "指引者" }
            ]
        }
        return json.dumps(mock_data, ensure_ascii=False)
    
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
    
    def _generate_mock_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        生成模拟场景内容
        """
        scene_name = context.get("sceneName", "新场景")
        style = params.get("style", "像素风")
        emotion = params.get("emotion", "治愈")
        
        return f"像素风格的{scene_name}，具有{emotion}氛围。背景包含树木、小径和远处的山丘。有可互动元素：神秘宝箱、友善NPC、隐藏通道。场景跳转关系：通往森林、村庄、洞穴。"
    
    def _generate_mock_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        生成模拟对话内容
        """
        character_name = context.get("characterName", "NPC")
        style = params.get("style", "像素风")
        emotion = params.get("emotion", "治愈")
        
        return f"{character_name}：\n- 你好，旅行者！\n- 这里最近有些奇怪的事情发生。\n- 也许你可以去问问村长。\n- 祝你好运！"
    
    def _generate_mock_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        生成模拟任务内容
        """
        task_name = context.get("taskName", "新任务")
        style = params.get("style", "像素风")
        emotion = params.get("emotion", "治愈")
        
        return f"任务名称：{task_name}\n触发条件：与村长对话\n完成条件：找到丢失的物品\n奖励：50经验值，10金币\n后续任务：解锁新区域\n任务描述：帮助村民找回丢失的重要物品，途中可能会遇到一些小挑战。"


class WenxinAIAdapter(BaseAIAdapter):
    """
    百度文心一言适配器实现 - 支持真实API调用
    """
    
    def __init__(self):
        self.api_key = AIConfig.WENXIN_API_KEY
        self.secret_key = AIConfig.WENXIN_SECRET_KEY
        self.model = AIConfig.WENXIN_MODEL
        self.timeout = AIConfig.AI_REQUEST_TIMEOUT
        self._access_token = None
        self._token_expires = 0
        if not self.api_key or not self.secret_key:
            print("警告: WENXIN_API_KEY 或 WENXIN_SECRET_KEY 环境变量未设置，将使用模拟数据")
    
    def _get_access_token(self) -> str:
        """获取文心一言API的access_token"""
        if self._access_token and time.time() < self._token_expires:
            return self._access_token
        
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        
        with httpx.Client(timeout=30) as client:
            response = client.post(url)
            response.raise_for_status()
            result = response.json()
            self._access_token = result["access_token"]
            self._token_expires = time.time() + result.get("expires_in", 86400) - 300
            return self._access_token
    
    def _get_model_endpoint(self) -> str:
        """获取模型对应的API端点"""
        model_endpoints = {
            "ernie-bot-4": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro",
            "ernie-bot": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
            "ernie-bot-turbo": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant",
        }
        return model_endpoints.get(self.model, model_endpoints["ernie-bot"])
    
    @retry_on_failure(max_retries=AIConfig.AI_MAX_RETRIES)
    def _call_wenxin_api(self, prompt: str) -> str:
        """调用文心一言API"""
        access_token = self._get_access_token()
        url = f"{self._get_model_endpoint()}?access_token={access_token}"
        
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            if "error_code" in result:
                raise Exception(f"文心一言API错误: {result.get('error_msg', '未知错误')}")
            return result["result"]
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """使用文心一言生成游戏原型"""
        if not self.api_key or not self.secret_key:
            print("使用模拟数据生成游戏原型...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
        
        try:
            print(f"调用文心一言API生成游戏原型...")
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_game_prompt(manuscript_data, params)
            response = self._call_wenxin_api(prompt)
            
            try:
                game_data = json.loads(response)
                game_data["gameId"] = f"game-{uuid.uuid4().hex[:8]}"
                game_data["gameName"] = manuscript_data.get("storyTitle", "未命名游戏")
                game_data["emotionalTone"] = params.get("emotion", "neutral")
                game_data["style"] = params.get("style", "pixel_art")
                game_data["createdAt"] = time.time()
                return game_data
            except json.JSONDecodeError:
                print("API响应解析失败，使用模拟数据...")
                return adapter._generate_mock_prototype(manuscript_data, params)
                
        except Exception as e:
            print(f"文心一言API调用失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
    
    def assist_with_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成场景"""
        if not self.api_key or not self.secret_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_scene_prompt(content, context, params)
            return self._call_wenxin_api(prompt)
        except Exception as e:
            print(f"场景生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
    
    def assist_with_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成对话"""
        if not self.api_key or not self.secret_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_dialog_prompt(content, context, params)
            return self._call_wenxin_api(prompt)
        except Exception as e:
            print(f"对话生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
    
    def assist_with_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助设计任务"""
        if not self.api_key or not self.secret_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_task_prompt(content, context, params)
            return self._call_wenxin_api(prompt)
        except Exception as e:
            print(f"任务生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)

class QianwenAIAdapter(BaseAIAdapter):
    """
    阿里通义千问适配器实现 - 支持真实API调用
    """
    
    def __init__(self):
        self.api_key = AIConfig.QIANWEN_API_KEY
        self.model = AIConfig.QIANWEN_MODEL
        self.timeout = AIConfig.AI_REQUEST_TIMEOUT
        if not self.api_key:
            print("警告: QIANWEN_API_KEY 环境变量未设置，将使用模拟数据")
    
    @retry_on_failure(max_retries=AIConfig.AI_MAX_RETRIES)
    def _call_qianwen_api(self, prompt: str) -> str:
        """调用通义千问API"""
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "input": {
                "messages": [{"role": "user", "content": prompt}]
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 4096
            }
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "Success":
                raise Exception(f"通义千问API错误: {result.get('message', '未知错误')}")
            return result["output"]["text"]
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """使用通义千问生成游戏原型"""
        if not self.api_key:
            print("使用模拟数据生成游戏原型...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
        
        try:
            print(f"调用通义千问API生成游戏原型...")
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_game_prompt(manuscript_data, params)
            response = self._call_qianwen_api(prompt)
            
            try:
                game_data = json.loads(response)
                game_data["gameId"] = f"game-{uuid.uuid4().hex[:8]}"
                game_data["gameName"] = manuscript_data.get("storyTitle", "未命名游戏")
                game_data["emotionalTone"] = params.get("emotion", "neutral")
                game_data["style"] = params.get("style", "pixel_art")
                game_data["createdAt"] = time.time()
                return game_data
            except json.JSONDecodeError:
                print("API响应解析失败，使用模拟数据...")
                return adapter._generate_mock_prototype(manuscript_data, params)
                
        except Exception as e:
            print(f"通义千问API调用失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
    
    def assist_with_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成场景"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_scene_prompt(content, context, params)
            return self._call_qianwen_api(prompt)
        except Exception as e:
            print(f"场景生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
    
    def assist_with_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成对话"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_dialog_prompt(content, context, params)
            return self._call_qianwen_api(prompt)
        except Exception as e:
            print(f"对话生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
    
    def assist_with_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助设计任务"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_task_prompt(content, context, params)
            return self._call_qianwen_api(prompt)
        except Exception as e:
            print(f"任务生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)


class ModelScopeAIAdapter(BaseAIAdapter):
    """
    魔搭社区适配器实现 - 使用DashScope API（与通义千问相同）
    魔搭社区赠送2000免费额度，适合国内用户使用
    """
    
    def __init__(self):
        self.api_key = AIConfig.MODELSCOPE_API_KEY
        self.model = AIConfig.MODELSCOPE_MODEL
        self.timeout = AIConfig.AI_REQUEST_TIMEOUT
        if not self.api_key:
            print("警告: MODELSCOPE_API_KEY 环境变量未设置，将使用模拟数据")
    
    @retry_on_failure(max_retries=AIConfig.AI_MAX_RETRIES)
    def _call_modelscope_api(self, prompt: str) -> str:
        """调用魔搭社区API（DashScope）"""
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "input": {
                "messages": [{"role": "user", "content": prompt}]
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 4096
            }
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            if "code" in result and result["code"] != "Success":
                raise Exception(f"魔搭API错误: {result.get('message', '未知错误')}")
            return result["output"]["text"]
    
    def generate_game_prototype(self, manuscript_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """使用魔搭社区生成游戏原型"""
        if not self.api_key:
            print("使用模拟数据生成游戏原型...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
        
        try:
            print(f"调用魔搭社区API生成游戏原型...")
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_game_prompt(manuscript_data, params)
            response = self._call_modelscope_api(prompt)
            
            try:
                game_data = json.loads(response)
                game_data["gameId"] = f"game-{uuid.uuid4().hex[:8]}"
                game_data["gameName"] = manuscript_data.get("storyTitle", "未命名游戏")
                game_data["emotionalTone"] = params.get("emotion", "neutral")
                game_data["style"] = params.get("style", "pixel_art")
                game_data["createdAt"] = time.time()
                return game_data
            except json.JSONDecodeError:
                print("API响应解析失败，使用模拟数据...")
                return adapter._generate_mock_prototype(manuscript_data, params)
                
        except Exception as e:
            print(f"魔搭API调用失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_prototype(manuscript_data, params)
    
    def assist_with_scene(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成场景"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_scene_prompt(content, context, params)
            return self._call_modelscope_api(prompt)
        except Exception as e:
            print(f"场景生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_scene(content, context, params)
    
    def assist_with_dialog(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助生成对话"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_dialog_prompt(content, context, params)
            return self._call_modelscope_api(prompt)
        except Exception as e:
            print(f"对话生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_dialog(content, context, params)
    
    def assist_with_task(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助设计任务"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_task_prompt(content, context, params)
            return self._call_modelscope_api(prompt)
        except Exception as e:
            print(f"任务生成失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_task(content, context, params)

    def assist_with_manuscript(self, content: str, context: Dict[str, Any], params: Dict[str, Any]) -> str:
        """AI辅助补全原稿表单"""
        if not self.api_key:
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_manuscript(content, context, params)
        
        try:
            adapter = OpenAIAIAdapter()
            prompt = adapter._build_manuscript_prompt(content, context, params)
            return self._call_modelscope_api(prompt)
        except Exception as e:
            print(f"原稿补全失败: {e}，使用模拟数据...")
            adapter = OpenAIAIAdapter()
            return adapter._generate_mock_manuscript(content, context, params)


class AIAdapterFactory:
    """
    AI适配器工厂类，用于创建不同类型的AI适配器
    支持: openai, wenxin, qianwen, modelscope
    """
    
    _adapters = {
        'openai': OpenAIAIAdapter,
        'wenxin': WenxinAIAdapter,
        'qianwen': QianwenAIAdapter,
        'modelscope': ModelScopeAIAdapter,
    }
    
    @staticmethod
    def create_adapter(adapter_type: str = None) -> BaseAIAdapter:
        """
        创建指定类型的AI适配器
        :param adapter_type: 适配器类型 ('openai', 'wenxin', 'qianwen', 'modelscope')
        :return: AI适配器实例
        """
        if adapter_type is None:
            adapter_type = AIConfig.AI_ADAPTER_TYPE
        
        adapter_type = adapter_type.lower()
        if adapter_type in AIAdapterFactory._adapters:
            return AIAdapterFactory._adapters[adapter_type]()
        else:
            raise ValueError(f"不支持的AI适配器类型: {adapter_type}，支持的类型: {list(AIAdapterFactory._adapters.keys())}")
    
    @staticmethod
    def get_available_adapters() -> List[str]:
        """获取所有可用的适配器类型"""
        return list(AIAdapterFactory._adapters.keys())
    
    @staticmethod
    def switch_adapter(adapter_type: str) -> BaseAIAdapter:
        """
        动态切换AI适配器
        :param adapter_type: 新的适配器类型
        :return: 新的AI适配器实例
        """
        global ai_adapter
        ai_adapter = AIAdapterFactory.create_adapter(adapter_type)
        print(f"已切换到 {adapter_type} 适配器")
        return ai_adapter


# 全局AI适配器实例
ai_adapter = AIAdapterFactory.create_adapter()