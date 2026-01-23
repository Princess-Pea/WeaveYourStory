import gradio as gr
from pydantic import BaseModel
import os
import json
from typing import Dict, Any

class PixelForgeApp:
    """
    PixelForge Web应用的Gradio封装
    支持团队协作开发的Web应用展示
    """
    
    def __init__(self):
        self.app_title = "PixelForge - 团队协作Web应用"
        self.description = "这是一个用于团队协作开发的Web应用项目，部署到魔搭创空间"
    
    def welcome_message(self, user_input: str = ""):
        """生成欢迎消息"""
        if user_input.strip():
            return f"欢迎来到 PixelForge, {user_input}! 这是一个用于团队协作开发的Web应用。"
        else:
            return "欢迎来到 PixelForge! 这是一个用于团队协作开发的Web应用。"
    
    def get_project_info(self) -> Dict[str, Any]:
        """获取项目信息"""
        info = {
            "name": "PixelForge",
            "version": "1.0.0",
            "description": "团队协作Web应用",
            "features": [
                "模块化设计，便于团队协作",
                "响应式布局，跨设备兼容",
                "云端部署，一键上线"
            ]
        }
        return info
    
    def run_gradio_app(self):
        """运行Gradio界面"""
        with gr.Blocks(title=self.app_title) as demo:
            gr.Markdown(f"# {self.app_title}")
            gr.Markdown(self.description)
            
            with gr.Row():
                with gr.Column():
                    name_input = gr.Textbox(label="输入您的姓名", placeholder="例如：张三")
                    greet_btn = gr.Button("获取欢迎信息")
                
                with gr.Column():
                    output = gr.Textbox(label="欢迎信息", interactive=False)
            
            greet_btn.click(
                fn=self.welcome_message,
                inputs=name_input,
                outputs=output
            )
            
            gr.Markdown("## 项目信息")
            project_info_btn = gr.Button("获取项目详情")
            project_output = gr.JSON(label="项目详情")
            
            project_info_btn.click(
                fn=self.get_project_info,
                inputs=None,
                outputs=project_output
            )
            
            gr.Markdown("## Web应用预览")
            gr.HTML("""
            <div style="border: 1px solid #ccc; padding: 20px; border-radius: 8px;">
                <h3>PixelForge Web应用</h3>
                <p>这是一个示例前端页面，展示了团队协作开发的能力。</p>
                <iframe src="./index.html" width="100%" height="400px" style="border: none;"></iframe>
            </div>
            """)
        
        return demo

# 创建应用实例
pixel_forge_app = PixelForgeApp()

# 定义主要函数接口
def modelscope_quickstart(name: str = ""):
    return pixel_forge_app.welcome_message(name)

# 创建Gradio界面
demo = pixel_forge_app.run_gradio_app()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False
    )