import uuid
import time
import threading
import json
import heapq
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable, List
from .ai_adapter import ai_adapter


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(Enum):
    """任务优先级枚举（数值越小优先级越高）"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass(order=True)
class TaskItem:
    """任务项数据类"""
    priority: int
    timestamp: float = field(compare=False)
    task_id: str = field(compare=False)
    content: str = field(compare=False)
    context: Dict[str, Any] = field(compare=False)
    params: Dict[str, Any] = field(compare=False)


class TaskManager:
    """
    增强型异步任务管理器
    支持: 任务优先级、任务队列、进度可视化、任务取消/暂停
    """
    
    def __init__(self, max_concurrent: int = 3):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_queue: List[TaskItem] = []
        self.max_concurrent = max_concurrent
        self.active_count = 0
        self.lock = threading.Lock()
        self.task_threads: Dict[str, threading.Thread] = {}
        self.cancel_flags: Dict[str, threading.Event] = {}
        self.pause_flags: Dict[str, threading.Event] = {}
        
        # 启动队列处理线程
        self.queue_processor = threading.Thread(target=self._process_queue, daemon=True)
        self.queue_processor.start()
    
    def _generate_id(self, prefix: str = "task") -> str:
        """生成唯一ID"""
        return f"{prefix}-{uuid.uuid4().hex[:8]}"
    
    def _process_queue(self):
        """队列处理线程"""
        while True:
            with self.lock:
                if self.task_queue and self.active_count < self.max_concurrent:
                    task_item = heapq.heappop(self.task_queue)
                    self._start_task_execution(task_item)
            time.sleep(0.5)
    
    def _start_task_execution(self, task_item: TaskItem):
        """启动任务执行"""
        task_id = task_item.task_id
        self.tasks[task_id]["status"] = TaskStatus.PROCESSING.value
        self.active_count += 1
        
        # 创建取消和暂停标志
        self.cancel_flags[task_id] = threading.Event()
        self.pause_flags[task_id] = threading.Event()
        self.pause_flags[task_id].set()  # 默认不暂停
        
        thread = threading.Thread(
            target=self._execute_task,
            args=(task_item,)
        )
        self.task_threads[task_id] = thread
        thread.start()
    
    def _execute_task(self, task_item: TaskItem):
        """执行任务"""
        task_id = task_item.task_id
        cancel_flag = self.cancel_flags.get(task_id)
        pause_flag = self.pause_flags.get(task_id)
        
        try:
            steps = 10
            for i in range(1, steps + 1):
                # 检查取消标志
                if cancel_flag and cancel_flag.is_set():
                    self.tasks[task_id]["status"] = TaskStatus.CANCELLED.value
                    self.tasks[task_id]["errorMsg"] = "任务已被取消"
                    print(f"任务 {task_id} 已取消")
                    return
                
                # 检查暂停标志
                if pause_flag:
                    pause_flag.wait()  # 如果被暂停则等待
                
                # 更新进度
                progress = int((i / steps) * 100)
                self.tasks[task_id]["progress"] = progress
                self.tasks[task_id]["currentStep"] = f"处理中... ({i}/{steps})"
                print(f"任务 {task_id} 进度: {progress}%")
                time.sleep(1)
            
            # 解析原稿内容并生成
            manuscript_data = json.loads(task_item.content)
            game_prototype = ai_adapter.generate_game_prototype(manuscript_data, task_item.params)
            
            self.tasks[task_id]["status"] = TaskStatus.COMPLETED.value
            self.tasks[task_id]["result"] = game_prototype
            self.tasks[task_id]["completedAt"] = time.time()
            print(f"任务 {task_id} 生成完成!")
            
        except json.JSONDecodeError as e:
            self.tasks[task_id]["status"] = TaskStatus.FAILED.value
            self.tasks[task_id]["errorMsg"] = f"JSON解析错误: {str(e)}"
            print(f"任务 {task_id} JSON解析失败: {str(e)}")
        except Exception as e:
            self.tasks[task_id]["status"] = TaskStatus.FAILED.value
            self.tasks[task_id]["errorMsg"] = str(e)
            print(f"任务 {task_id} 生成失败: {str(e)}")
        finally:
            with self.lock:
                self.active_count -= 1
                # 清理标志
                self.cancel_flags.pop(task_id, None)
                self.pause_flags.pop(task_id, None)
                self.task_threads.pop(task_id, None)
    
    def submit_task(
        self,
        content: str,
        context: Dict[str, Any],
        params: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        task_id: str = None
    ) -> tuple:
        """
        提交任务到队列
        :return: (request_id, task_id)
        """
        if task_id is None:
            task_id = self._generate_id("task")
        request_id = self._generate_id("req")
        
        # 初始化任务状态
        self.tasks[task_id] = {
            "status": TaskStatus.QUEUED.value,
            "progress": 0,
            "result": None,
            "priority": priority.value,
            "createdAt": time.time(),
            "currentStep": "等待处理",
            "errorMsg": None
        }
        
        # 创建任务项并加入队列
        task_item = TaskItem(
            priority=priority.value,
            timestamp=time.time(),
            task_id=task_id,
            content=content,
            context=context,
            params=params
        )
        
        with self.lock:
            heapq.heappush(self.task_queue, task_item)
        
        return request_id, task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id not in self.tasks:
            return False
        
        status = self.tasks[task_id]["status"]
        
        # 如果任务还在队列中，直接移除
        if status == TaskStatus.QUEUED.value:
            with self.lock:
                self.task_queue = [t for t in self.task_queue if t.task_id != task_id]
                heapq.heapify(self.task_queue)
            self.tasks[task_id]["status"] = TaskStatus.CANCELLED.value
            return True
        
        # 如果任务正在执行，设置取消标志
        if status == TaskStatus.PROCESSING.value:
            if task_id in self.cancel_flags:
                self.cancel_flags[task_id].set()
                # 如果任务被暂停，先恢复以便检查取消标志
                if task_id in self.pause_flags:
                    self.pause_flags[task_id].set()
                return True
        
        return False
    
    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        if task_id not in self.tasks:
            return False
        
        if self.tasks[task_id]["status"] == TaskStatus.PROCESSING.value:
            if task_id in self.pause_flags:
                self.pause_flags[task_id].clear()
                self.tasks[task_id]["status"] = TaskStatus.PAUSED.value
                return True
        return False
    
    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        if task_id not in self.tasks:
            return False
        
        if self.tasks[task_id]["status"] == TaskStatus.PAUSED.value:
            if task_id in self.pause_flags:
                self.pause_flags[task_id].set()
                self.tasks[task_id]["status"] = TaskStatus.PROCESSING.value
                return True
        return False
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        return self.tasks.get(task_id, {"status": "not_found", "progress": 0})
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """获取所有任务"""
        return self.tasks.copy()
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        return {
            "queued_count": len(self.task_queue),
            "active_count": self.active_count,
            "max_concurrent": self.max_concurrent,
            "total_tasks": len(self.tasks)
        }
    
    def clear_completed_tasks(self) -> int:
        """清理已完成的任务"""
        count = 0
        completed_statuses = [TaskStatus.COMPLETED.value, TaskStatus.CANCELLED.value, TaskStatus.FAILED.value]
        task_ids = list(self.tasks.keys())
        for task_id in task_ids:
            if self.tasks[task_id]["status"] in completed_statuses:
                del self.tasks[task_id]
                count += 1
        return count


# 全局任务管理器实例
task_manager = TaskManager()

# 兼容旧接口
tasks = task_manager.tasks


def generate_id(prefix="req"):
    return task_manager._generate_id(prefix)


def simulate_ai_generation(task_id, content, context, params):
    """兼容旧接口的模拟生成函数"""
    task_manager.submit_task(content, context, params, task_id=task_id)


def start_async_ai_task(content, context, params, task_id=None, priority=TaskPriority.NORMAL):
    """启动异步AI任务（增强版）"""
    return task_manager.submit_task(content, context, params, priority=priority, task_id=task_id)


def get_task_status(task_id):
    """获取任务状态"""
    return task_manager.get_task_status(task_id)


def cancel_task(task_id):
    """取消任务"""
    return task_manager.cancel_task(task_id)


def pause_task(task_id):
    """暂停任务"""
    return task_manager.pause_task(task_id)


def resume_task(task_id):
    """恢复任务"""
    return task_manager.resume_task(task_id)


def get_queue_status():
    """获取队列状态"""
    return task_manager.get_queue_status()
