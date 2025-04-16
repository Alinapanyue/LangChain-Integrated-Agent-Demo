from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings  # 修改这行
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA

def create_qa_system(file_path):
    # 1. 加载文档
    loader = TextLoader(file_path)
    documents = loader.load()
    
    # 2. 创建向量存储
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # 3. 创建问答链
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa