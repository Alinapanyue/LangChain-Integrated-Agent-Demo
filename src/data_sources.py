# data_sources.py
import requests
import sqlite3
from typing import Dict, Any
from bs4 import BeautifulSoup

class DataSources:
    def __init__(self):
        self.db_conn = sqlite3.connect('example.db')
        self.api_key = "your_api_key"
        self._setup_database()  # 添加这行
    
    def _setup_database(self):
        """初始化数据库结构"""
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        # 添加一些测试数据
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, name, email)
            VALUES (1, "测试用户", "test@example.com")
        ''')
        self.db_conn.commit()
    
    def query_api(self, endpoint: str) -> Dict[str, Any]:
        """调用外部 API"""
        # 模拟 API 调用
        if "天气" in endpoint:
            return {"weather": "晴天", "temperature": "25°C"}
        return {"message": "API 调用成功", "endpoint": endpoint}
    
    def query_database(self, query_type: str) -> list:
        """查询数据库"""
        cursor = self.db_conn.cursor()
        if query_type == "用户信息":
            cursor.execute("SELECT * FROM users")
        else:
            return [("未知查询类型",)]
        return cursor.fetchall()
    
    def save_to_database(self, data: Dict[str, Any]):
        """保存数据到数据库"""
        # 实现保存逻辑
        pass

class RockwellDataSource:
    def __init__(self):
        self.base_url = "https://www.rockwellautomation.com.cn"
        # 创建或连接SQLite数据库
        self.conn = sqlite3.connect('rockwell_data.db')
        self.create_tables()
        
    def create_tables(self):
        """创建数据库表"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                query TEXT PRIMARY KEY,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def search_website(self, query):
        """搜索Rockwell官网"""
        # 先检查缓存
        cursor = self.conn.cursor()
        cursor.execute("SELECT result FROM search_cache WHERE query = ?", (query,))
        cached = cursor.fetchone()
        
        if cached:
            print("从缓存获取结果")
            return cached[0]
        
        # 如果没有缓存，爬取网站
        try:
            search_url = f"{self.base_url}/search?query={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(search_url, headers=headers)
            
            if response.status_code == 200:
                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取搜索结果
                search_results = []
                result_elements = soup.select('.search-result-item')  # 根据实际网站调整选择器
                
                for element in result_elements[:5]:  # 只取前5个结果
                    title = element.select_one('.title').text.strip()
                    description = element.select_one('.description').text.strip()
                    url = element.select_one('a')['href']
                    
                    search_results.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })
                
                # 转为字符串以便存储
                result_str = str(search_results)
                
                # 存入缓存
                cursor.execute("INSERT INTO search_cache (query, result) VALUES (?, ?)", 
                             (query, result_str))
                self.conn.commit()
                
                return result_str
            else:
                return f"网站请求失败，状态码: {response.status_code}"
        
        except Exception as e:
            return f"搜索过程出错: {str(e)}"