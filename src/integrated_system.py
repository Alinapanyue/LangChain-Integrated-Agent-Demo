# integrated_system.py
from workflow_advanced import create_advanced_workflow
from data_sources import DataSources
from rpa_integration import RPATools

class IntegratedAgent:
    def __init__(self):
        self.workflow = create_advanced_workflow()
        self.data_sources = DataSources()
        self.rpa_tools = RPATools()
    
    def process_request(self, user_input: str):
        try:
            # 1. 根据输入内容直接处理不同类型的请求
            if "数据库" in user_input or "用户信息" in user_input:
                data = self.data_sources.query_database("用户信息")
                return f"查询到的用户信息：{data}"
                
            elif "天气" in user_input or "API" in user_input:
                data = self.data_sources.query_api("天气查询")
                return f"天气信息：{data}"
                
            elif "浏览器" in user_input:
                result = self.rpa_tools.automate_browser("https://example.com")
                return f"浏览器操作：{result}"
            
            # 2. 如果没有特定关键词，使用工作流处理
            return self.workflow.run(user_input)
            
        except Exception as e:
            return f"处理请求时出错: {str(e)}"