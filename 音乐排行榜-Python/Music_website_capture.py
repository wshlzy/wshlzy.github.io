import requests
import os
import xlwt
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from datetime import datetime

# 使用requests库抓取静态数据（直接从服务器请求HTML页面或API数据，而不渲染JavaScript，执行速度极快，）
def fetch_html_with_bs(url):
    """Fetch the HTML content from the given website URL."""
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"}
    response = requests.get(url, headers=head)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        raise Exception(f"Failed to fetch the webpage: {url}")
    
# 使用Selenium库预加载，抓取动态数据（系统控制打开浏览器加载内容，速度较慢。它需要加载整个页面，包括所有的CSS、JavaScript、图片）
def fetch_dynamic_html(url, iframe_name):
    webdriver_path = "webdriver/msedgedriver.exe"
    edge_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    edge_options.add_argument(f'user-agent={user_agent}')

    service = Service(webdriver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    
    driver.get(url)
    if iframe_name != None:
        driver.switch_to.frame(iframe_name)

    time.sleep(random.uniform(2,5))
    html_content = driver.page_source
    driver.quit()

    html_content = BeautifulSoup(html_content, "html.parser")
    return html_content

# data_list 包含：[网站名，网址，歌曲样本tag，歌手样本tag，榜单更新时间tag，榜单标题tag，静态/动态数据(0/1)，0: None/1: iframe类名].
def write_LIST_into_excel(index, url, data_list):
    if data_list[6] == 0:
        web_content = fetch_html_with_bs(url)
    else:
        web_content = fetch_dynamic_html(url, data_list[7])

    # 通过手动标记的歌曲样本tag，歌手tag，时间tag和榜单标题tag，从抓取的数据源中筛选数据
    song_names = web_content.select(data_list[2])
    artists = web_content.select(data_list[3])
    # if data_list[4] is not None:
    #     time_info = web_content.select_one(data_list[4]).text
    # else:
    #     time_info = datetime.now().date()
    # LIST = web_content.select_one(data_list[5]).text
    sheet_names = ['新歌榜', '热歌榜', '飙升榜']
    LIST = sheet_names[index]

    # 创建一个 DataFrame 存储数据
    data = {
        'Song Name': [],
        'Artist': []
    }

    # 网易云音乐存在污染数据的设定
    if data_list[0] == "NetEase Music":
        for item in song_names:
            data['Song Name'].append(item.get("title"))
    elif data_list[0] == "QQ Music":
        for item in song_names:
            data['Song Name'].append(item.get("title"))
    else:
        print(song_names)
        for item in song_names:
            data['Song Name'].append(item.get_text())

    # 处理歌手信息
    flag = 0
    if data_list[0] == "NetEase Music":
        for item in artists:
            if flag != 0:
                flag -= 1
                continue
            temp = item.get("title")
            while item.find_next_sibling() is not None:
                temp = f'{temp}/{item.find_next_sibling().get("title")}'
                item = item.find_next_sibling()
                flag += 1
            data['Artist'].append(temp)
    else:
        for item in artists:
            if flag != 0:
                flag -= 1
                continue
            temp = item.get_text()
            while item.find_next_sibling() is not None:
                temp = f'{temp}/{item.find_next_sibling().get_text()}'
                item = item.find_next_sibling()
                flag += 1
            data['Artist'].append(temp)

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 保存 DataFrame 为 Excel
    folder_name = f'{data_list[0]}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = f'{data_list[0]} {LIST}.xlsx'
    output_path = os.path.join(folder_name, file_name)
    df.to_excel(output_path, index=False, sheet_name=f'{data_list[0]} {LIST}')

def main():
    # data_list 包含：[网站名,网址，歌曲样本tag，歌手样本tag，榜单更新时间tag，榜单标题tag，静态/动态数据(0/1)，if 1 iframe类名].
    QQ_example = ['QQ Music', # 2025/07/16记录：QQ音乐排行榜部分已完成静态到动态内容的转换
                {'urls': ['https://y.qq.com/n/ryqq/toplist/27', 
                            'https://y.qq.com/n/ryqq/toplist/26', 
                            'https://y.qq.com/n/ryqq/toplist/62']}, 
                'span[class="songlist__songname_txt"] a:nth-of-type(2)', # 需要定期更新
                'a[class="playlist__author"]',
                'span[class="toplist_switch__data"]', 
                'h1[class="toplist__tit"]', 
                1,
                None]

    NetEase_example = ['NetEase Music',
                    {'urls': ['https://music.163.com/#/discover/toplist?id=3779629',
                                'https://music.163.com/#/discover/toplist?id=3778678',
                                'https://music.163.com/#/discover/toplist?id=19723756']}, 
                    'b[title]', # 需要定期更新
                    'div[class="text"]', # 需要定期更新
                    'span[class="sep s-fc3"]', 
                    'h2[class="f-ff2"]', 
                    1, 
                    "g_iframe"]

    Kugou_example = ['Kugou Music',
                    {'urls': ['https://www.kugou.com/yy/rank/home/1-33162.html?from=rank',
                            'https://www.kugou.com/yy/rank/home/1-6666.html?from=rank',
                            'https://www.kugou.com/yy/rank/home/1-8888.html?from=rank']}, 
                    'a[class="pc_temp_songname"]', 
                    'a[class="pc_temp_songname"] span', 
                    'span[class="rank_update"]', 
                    'div[class="pc_temp_title"] h3', 
                    0]

    Apple_example = ['Apple Music', # 苹果音乐网站的类名会定期更换
                    {'urls': ['https://music.apple.com/cn/room/6748489592',                  
                            'https://music.apple.com/cn/room/6748482691']}, 
                    'div[data-testid="track-title"]', 
                    'div[data-testid="track-title-by-line"] span', 
                    None,  # 如果页面中不存在榜单更新时间，设置为None，生成数据时将系统时间作为表单更新时间
                    'div[data-testid="header-component-model"] h1',
                    1, 
                    None]

    Combine_example = [QQ_example, NetEase_example, Kugou_example, Apple_example]

    os.chdir(os.path.dirname(os.path.abspath(__file__))) # 切换路径到当前文件夹下

    try:
        for example in Combine_example:
            for index, url in enumerate(example[1]['urls']):
                write_LIST_into_excel(index, url, example)
                time.sleep(random.uniform(1,3)) # 同一IP频繁发送请求，可能会触发反爬虫机制，在每次发送请求时加入随机的停顿，减缓判定
    except Exception as e:
        print(f'error occured: {e}')
    finally:
        print("抓取数据已完成")
    
    return

main()