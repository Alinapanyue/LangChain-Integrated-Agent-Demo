# LangChain Integrated Agent Demo

基于 LangChain 开发的非常简单的智能代理系统，集成了 RAG、工作流和 RPA 功能。

## 功能模块

- RAG 系统：文档问答
- 智能工作流：问题分类、工具调用
- 数据源集成：数据库、API
- RPA 自动化集成

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/Alinapanyue/LangChain-Integrated-Agent-Demo.git
cd LangChain-Integrated-Agent-Demo

# 2. 安装依赖
pip install requests python-dotenv langchain openai faiss-cpu

# 3. 配置环境变量
# 创建 .env 文件并添加，这里使用了openai的api key：
OPENAI_API_KEY=your_api_key

# 4. 运行测试
python src/run_tests.py
```

## 项目结构

```
src/
├── rag_demo.py          # RAG 系统
├── workflow_demo.py     # 基础工作流
├── workflow_advanced.py # 高级工作流
├── data_sources.py     # 数据源集成
├── rpa_integration.py  # RPA 集成
└── integrated_system.py # 系统集成
```