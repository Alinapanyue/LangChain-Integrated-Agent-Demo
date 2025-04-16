import os
from dotenv import load_dotenv
load_dotenv()

def test_rag():
    print("\n=== 测试 RAG 系统 ===")
    from rag_demo import create_qa_system
    
    file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_doc.txt")
    qa = create_qa_system(file_path)
    
    test_questions = [
        "LangChain 是什么？",
        "LangChain 有哪些主要功能？"
    ]
    
    for question in test_questions:
        print(f"\n问题：{question}")
        print(f"回答：{qa.run(question)}")

def test_advanced_workflow():
    print("\n=== 测试高级工作流系统 ===")
    from workflow_advanced import create_advanced_workflow
    
    agent = create_advanced_workflow()
    test_inputs = [
        "我需要帮助，不知道从哪里开始",
        "帮我搜索 LangChain 的主要功能",
        "这个问题应该属于什么类型"
    ]
    
    for input_text in test_inputs:
        print(f"\n输入：{input_text}")
        print(f"结果：{agent.run(input_text)}")

def test_integrated_system():
    print("\n=== 测试集成系统 ===")
    from integrated_system import IntegratedAgent
    
    agent = IntegratedAgent()
    test_cases = [
        "请查询数据库中的用户信息",
        "请帮我查看现在的天气情况",
        "请帮我打开浏览器并搜索信息"
    ]
    
    for case in test_cases:
        print(f"\n测试用例：{case}")
        result = agent.process_request(case)
        print(f"结果：{result}")

if __name__ == "__main__":
    print("开始测试...")
    
    try:
        test_rag()
    except Exception as e:
        print("RAG 测试失败:", str(e))
    
    try:
        test_advanced_workflow()
    except Exception as e:
        print("高级工作流测试失败:", str(e))
    
    try:
        test_integrated_system()
    except Exception as e:
        print("集成系统测试失败:", str(e))