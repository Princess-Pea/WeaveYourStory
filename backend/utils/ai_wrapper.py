import uuid
import time
import threading
import json
from .ai_adapter import ai_adapter

# 模拟异步任务存储
tasks = {}

def generate_id(prefix="req"):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def simulate_ai_generation(task_id, content, context, params):
    """
    模拟AI生成过程的异步函数
    """
    tasks[task_id] = {"status": "processing", "progress": 0, "result": None}
    
    # 模拟生成步骤
    steps = 10
    for i in range(1, steps + 1):
        time.sleep(2)  # 模拟耗时操作
        progress = int((i / steps) * 100)
        tasks[task_id]["progress"] = progress
        
        # 更新任务状态
        tasks[task_id]["progress"] = progress
        
        print(f"任务 {task_id} 进度: {progress}%")
    
    try:
        # 解析原稿内容
        manuscript_data = json.loads(content)
        
        # 使用AI适配器生成游戏原型
        game_prototype = ai_adapter.generate_game_prototype(manuscript_data, params)
        
        # 生成模拟结果（像素风游戏雏形数据）
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = game_prototype
        
        print(f"任务 {task_id} 生成完成!")
        
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["errorMsg"] = str(e)
        print(f"任务 {task_id} 生成失败: {str(e)}")

def start_async_ai_task(content, context, params, task_id=None):
    if task_id is None:
        task_id = generate_id("task")
    request_id = generate_id("req")
    
    # 开启后台线程模拟AI
    thread = threading.Thread(target=simulate_ai_generation, args=(task_id, content, context, params))
    thread.start()
    
    return request_id, task_id

def get_task_status(task_id):
    return tasks.get(task_id, {"status": "not_found", "progress": 0})
