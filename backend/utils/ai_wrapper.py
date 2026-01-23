import uuid
import time
import threading

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
    steps = 5
    for i in range(1, steps + 1):
        time.sleep(2)  # 模拟耗时操作
        tasks[task_id]["progress"] = int((i / steps) * 100)
        
    # 生成模拟结果（像素风游戏雏形数据）
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["result"] = {
        "game_title": f"生成的游戏: {content[:10]}...",
        "scenes": [
            {"id": "start", "text": "你在一个阴暗的森林里醒来。", "options": [{"text": "往北走", "next": "forest_north"}]},
            {"id": "forest_north", "text": "你看到一个发光的像素方块。", "options": [{"text": "捡起来", "next": "end"}]},
            {"id": "end", "text": "游戏结束，你获得了神秘力量。", "options": []}
        ],
        "style": params.get("style", "classic_pixel")
    }

def start_async_ai_task(content, context, params):
    task_id = generate_id("task")
    request_id = generate_id("req")
    
    # 开启后台线程模拟AI
    thread = threading.Thread(target=simulate_ai_generation, args=(task_id, content, context, params))
    thread.start()
    
    return request_id, task_id

def get_task_status(task_id):
    return tasks.get(task_id, {"status": "not_found", "progress": 0})
