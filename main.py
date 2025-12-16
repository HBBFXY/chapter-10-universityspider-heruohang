import requests
from bs4 import BeautifulSoup
import csv
import time

class UniversityRankingSpider:
    """中国大学排名爬虫类，支持翻页爬取"""
    def __init__(self, base_url, total_pages):
        self.base_url = base_url  # 排名页面基础URL
        self.total_pages = total_pages  # 总页数
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.universities = []  # 存储爬取的高校信息

    def get_page_data(self, page):
        """爬取单页的高校排名数据"""
        try:
            # 构造带分页的URL（需根据实际网站的分页参数调整，此处为示例）
            url = f"{self.base_url}?page={page}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 抛出HTTP错误
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 解析高校信息（需根据目标网站的HTML结构调整选择器，此处为通用示例）
            # 请根据实际爬取的网站修改以下解析逻辑
            university_items = soup.select(".university-item")  # 示例选择器，需替换
            for item in university_items:
                rank = item.select_one(".rank").text.strip() if item.select_one(".rank") else "无"
                name = item.select_one(".name").text.strip() if item.select_one(".name") else "无"
                location = item.select_one(".location").text.strip() if item.select_one(".location") else "无"
                score = item.select_one(".score").text.strip() if item.select_one(".score") else "无"
                
                self.universities.append({
                    "排名": rank,
                    "学校名称": name,
                    "所在地区": location,
                    "综合得分": score
                })
            print(f"第{page}页数据爬取完成，共获取{len(university_items)}所高校信息")
        
        except Exception as e:
            print(f"第{page}页爬取失败：{str(e)}")

    def crawl(self):
        """批量爬取所有页面的高校数据"""
        print("开始爬取中国大学排名数据...")
        for page in range(1, self.total_pages + 1):
            self.get_page_data(page)
            time.sleep(1)  # 延迟1秒，避免请求过快被反爬
        print(f"爬取完成！共获取{len(self.universities)}所高校的排名信息")

    def save_to_csv(self, filename="中国大学排名.csv"):
        """将爬取的数据保存为CSV文件"""
        if not self.universities:
            print("无数据可保存")
            return
        
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            fieldnames = ["排名", "学校名称", "所在地区", "综合得分"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.universities)
        print(f"数据已保存至{filename}文件")

# 主程序执行
if __name__ == "__main__":
    # 注意：需替换为实际的中国大学排名网站基础URL和总页数
    # 示例：假设目标网站分页参数为page，总共有20页（对应近600所高校，每页30条）
    BASE_URL = "https://example.com/university-ranking"  # 替换为真实排名网站URL
    TOTAL_PAGES = 20  # 根据实际页数调整（近600所高校，按每页30条计算为20页）
    
    spider = UniversityRankingSpider(BASE_URL, TOTAL_PAGES)
    spider.crawl()
    spider.save_to_csv()# 在这里编写代码
