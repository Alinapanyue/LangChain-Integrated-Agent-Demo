from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

def search_function(query):
    return """LangChain 是一个强大的 AI 开发框架，主要功能包括：
    1. 大语言模型集成和链式调用
    2. RAG (检索增强生成)系统
    3. Agent 和工作流自动化
    4. 多数据源集成和向量存储
    5. 提示词工程和模板管理"""

def create_workflow():
    tools = [
        Tool(
            name="Search",
            func=search_function,
            description="用于搜索 LangChain 相关信息的工具"
        ),
    ]
    
    agent = initialize_agent(
        tools, 
        OpenAI(), 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent