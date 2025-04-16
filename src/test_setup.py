from dotenv import load_dotenv
from langchain_openai import OpenAI  # 新的导入方式
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 加载环境变量
load_dotenv()

def test_connection():
    try:
        # 创建 LLM
        llm = OpenAI()
        
        # 创建提示模板
        prompt = PromptTemplate(
            input_variables=["question"],
            template="请用简短的话回答：{question}"
        )
        
        # 创建新式链式调用
        chain = prompt | llm | StrOutputParser()
        
        # 测试调用
        response = chain.invoke({"question": "今天天气怎么样？"})
        print("连接测试成功！")
        print("AI回复:", response)
        
    except Exception as e:
        print("发生错误:", str(e))

if __name__ == "__main__":
    test_connection()