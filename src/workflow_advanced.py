# workflow_advanced.py
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from workflow_demo import search_function  

def classify_question(query):
    """问题分类工具"""
    return "这是一个关于 [分类结果] 的问题"

def user_guide(query):
    """用户引导工具"""
    return "我可以帮您：\n1. 搜索信息\n2. 分类问题\n3. 查询数据"

def create_advanced_workflow():
    tools = [
        Tool(
            name="Search",
            func=search_function,
            description="用于搜索 LangChain 相关信息"
        ),
        Tool(
            name="QuestionClassifier",
            func=classify_question,
            description="对用户问题进行分类"
        ),
        Tool(
            name="UserGuide",
            func=user_guide,
            description="提供用户引导和帮助"
        )
    ]
    
    # 添加记忆功能
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    agent = initialize_agent(
        tools, 
        OpenAI(), 
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    
    return agent