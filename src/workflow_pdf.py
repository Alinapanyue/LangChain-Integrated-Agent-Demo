from rag_pdf import create_qa_chain, answer_question
import re

def classify_question(question):
    """
    根据问题内容将其分类为网络相关、电机相关或一般问题
    """
    # 网络相关关键词
    network_keywords = ['网络', '以太网', 'EtherNet', 'IP', '通信', '连接', '端口', '协议', '网口']
    
    # 电机相关关键词
    motor_keywords = ['电机', '伺服', '转速', '扭矩', '编码器', '旋转', '驱动', '马达']
    
    # 产品搜索关键词 - 增加更多关键词
    search_keywords = ['产品', '最新', '解决方案', '自动化', '数字化', '软件', '型号', '购买', 
                     'Studio', 'studio', '5000', '支持', '获取', '服务']
    
    # 先检查搜索关键词
    for keyword in search_keywords:
        if keyword in question:
            return "search"
    
    # 检查是否包含网络关键词
    for keyword in network_keywords:
        if keyword.lower() in question.lower():
            return "network"
    
    # 检查是否包含电机关键词
    for keyword in motor_keywords:
        if keyword.lower() in question.lower():
            return "motor"
    
    # 默认为一般问题
    return "general"

def create_pdf_workflow():
    """
    创建包含分类和RAG功能的工作流
    """
    # 预先加载两个PDF的QA链
    network_qa = create_qa_chain("src/test_data/enet-um001_-zh-p.pdf", max_pages=5)
    motor_qa = create_qa_chain("src/test_data/smotor-um002_-zh-p.pdf", max_pages=5)
    
    def process_question(question):
        """处理用户问题的内部函数"""
        category = classify_question(question)
        
        if category == "network":
            print("这是一个网络相关问题，使用以太网手册回答...")
            return answer_question(network_qa, question)
        
        elif category == "motor":
            print("这是一个电机相关问题，使用伺服电机手册回答...")
            return answer_question(motor_qa, question)
        
        else:
            return "您的问题不够明确。请明确说明是关于以太网配置还是伺服电机的问题，以便我提供更准确的回答。"
    
    return process_question

def user_guide():
    """提供用户引导信息"""
    return """
    您好！我可以帮您回答关于Rockwell的问题，包括：
    1. EtherNet/IP网络配置和通信相关问题
    2. 伺服电机相关问题
    
    请明确您的问题属于哪个领域，这样我能提供更准确的回答。
    """

if __name__ == "__main__":
    workflow = create_pdf_workflow()
    
    print(user_guide())
    
    # 测试一些示例问题
    test_questions = [
        "EtherNet/IP网络如何配置？",
        "伺服电机的主要特点是什么？",
        "如何连接网络端口？",
        "能告诉我如何选择合适的伺服电机吗？",
        "产品的使用寿命是多久？"  # 一般问题
    ]
    
    for question in test_questions:
        print("\n问题:", question)
        print("回答:", workflow(question))
