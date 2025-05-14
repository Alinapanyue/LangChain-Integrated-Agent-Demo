# rag_pdf.py
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import re
import os

# 首先安装必要包: pip install pytesseract pdf2image pillow
# 注意：还需要安装Tesseract OCR引擎(https://github.com/tesseract-ocr/tesseract)
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract tesseract-lang
# 中文支持: brew install tesseract-chi-sim
# 使用 Homebrew 安装 Poppler
# brew install poppler
# 确认安装成功
# which pdftoppm

from pdf2image import convert_from_path
import pytesseract

load_dotenv()

def clean_text(text):
    """基础文本清理"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_pdf_text_with_ocr(pdf_path, max_pages=3):
    """使用OCR从PDF提取文本"""
    texts = []
    
    try:
        # 将PDF转换为图像，可能需要安装poppler
        # Mac: brew install poppler
        # Windows: 下载poppler，添加到PATH
        images = convert_from_path(pdf_path, first_page=1, last_page=max_pages)
        
        # OCR每个页面
        for i, image in enumerate(images):
            try:
                # 使用pytesseract进行OCR (支持中文)
                # 需要安装中文语言包：tesseract-chi-sim
                text = pytesseract.image_to_string(image, lang='chi_sim')
                if text and text.strip():
                    clean = clean_text(text)
                    if clean:
                        texts.append(clean)
                        print(f"成功OCR识别第 {i+1} 页内容，长度: {len(clean)} 字符")
            except Exception as e:
                print(f"OCR处理第 {i+1} 页时出错: {str(e)}")
    except Exception as e:
        print(f"PDF转图像出错: {str(e)}")
    
    return "\n\n".join(texts)

def create_qa_chain(pdf_path, max_pages=3):
    """创建一个简单的问答链，不使用向量存储"""
    # 提取文本
    text = extract_pdf_text_with_ocr(pdf_path, max_pages)
    if not text:
        raise ValueError("未能从PDF中提取任何文本")
    
    # 截取内容（避免超出上下文窗口）
    max_text_length = 8000  # 适当减小，OCR可能产生较长文本
    if len(text) > max_text_length:
        text = text[:max_text_length] + "..."
        print(f"文本已截断至{max_text_length}字符，避免超出模型限制")
    
    # 创建提示模板
    template = """
    你是一个帮助理解技术文档的AI助手。请基于下面的文档内容回答问题。
    如果无法从文档中找到答案，请明确说明。

    文档内容:
    {context}

    问题: {question}

    回答:
    """
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )
    
    # 创建LLM链
    llm = OpenAI(temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return {
        "chain": chain,
        "context": text
    }

def answer_question(qa_data, question):
    """使用QA链回答问题"""
    return qa_data["chain"].run(context=qa_data["context"], question=question)

if __name__ == "__main__":
    # 尝试电机手册
    pdf_path = "src/test_data/enet-um001_-zh-p.pdf"
    
    try:
        qa_data = create_qa_chain(pdf_path, max_pages=3)
        question = "这个手册说了什么？"
        answer = answer_question(qa_data, question)
        print("\n回答:")
        print(answer)
    except Exception as e:
        print(f"错误: {str(e)}")