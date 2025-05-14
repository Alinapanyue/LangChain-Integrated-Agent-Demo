from workflow_pdf import classify_question, create_pdf_workflow, user_guide
from data_sources_rockwell import RockwellDataSources
from rpa_integration import RockwellRPA

class RockwellIntegratedSystem:
    def __init__(self):
        print("初始化Rockwell集成系统...")
        
        # 初始化PDF工作流
        self.pdf_workflow = create_pdf_workflow()
        
        # 初始化数据源
        self.data_sources = RockwellDataSources()
        
        # 初始化RPA工具
        self.rpa = RockwellRPA()
    
    def process_question(self, question, user_email=None):
        """处理用户问题的主函数"""
        # 1. 分类问题
        category = classify_question(question)
        
        # 检查"Studio"关键词 - 添加特殊处理
        if "Studio" in question or "studio" in question:
            category = "search"  # 强制设为搜索类别
        
        # 2. 先尝试从数据库查询 - 修改处理顺序，优先使用数据库
        db_results = self.data_sources.query_database(question)
        
        # 3. 如果数据库有结果，直接使用
        if db_results:
            answer = f"根据我们的知识库：\n{db_results[0]['answer']}"
        else:
            # 4. 如果数据库没有结果，根据分类处理
            if category == "search" or category == "general":
                print("识别为一般搜索问题，尝试从官网获取信息...")
                # 从官网搜索
                web_results = self.data_sources.search_website(question)
                
                if web_results:
                    web_info = "\n官网相关信息：\n"
                    for result in web_results:
                        web_info += f"- {result['title']}\n  链接: {result['url']}\n  描述: {result['snippet']}\n"
                    
                    # 直接使用官网信息作为回答
                    answer = f"您询问的是关于'{question}'的信息。{web_info}\n\n如需了解更多具体技术细节，可以明确询问网络配置或伺服电机方面的问题。"
            else:
                # 5. 使用PDF工作流获取主要回答
                answer = self.pdf_workflow(question)
        
        # 6. 如果提供了邮箱，发送邮件
        if user_email:
            cat_name = "以太网/IP网络" if category == "network" else "伺服电机" if category == "motor" else "一般问题"
            email_content = self.rpa.format_answer_email(question, answer, cat_name)
            success, message = self.rpa.send_email(user_email, "Rockwell问题回答", email_content)
            if success:
                answer += "\n\n回答已通过邮件发送至您的邮箱。"
        
        return answer

if __name__ == "__main__":
    # 初始化系统
    system = RockwellIntegratedSystem()
    
    # 打印用户引导
    print(user_guide())
    
    # 处理用户问题
    while True:
        question = input("\n请输入您的问题 (输入'退出'结束): ")
        if question.lower() in ['退出', 'exit', 'quit']:
            break
            
        # 询问是否需要邮件回复
        email_option = input("是否需要通过邮件接收回答？(y/n): ")
        user_email = None
        if email_option.lower() == 'y':
            user_email = input("请输入您的邮箱地址: ")
        
        # 处理问题并输出回答
        answer = system.process_question(question, user_email)
        print("\n回答:")
        print(answer)
