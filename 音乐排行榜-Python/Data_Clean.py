import os
import pandas as pd
import re

# 清洗歌手名称，去掉 "-" 及其后面的内容
# 输入：字符串（未清洗的歌手名称）
# 输出：字符串（已清洗的歌手名称）
def clean_artist_name(artist_name: str):
    if not isinstance(artist_name, str):
        artist_name = str(artist_name)

    patterns = [
        # 更安全的反斜杠替换
        (re.compile(r'[、/]'), r'\\'),  # 使用原始字符串标记替换值
        
        # 改进的ft/feat匹配
        (re.compile(r'\s+ft(?:\.|\s+|$).*', re.IGNORECASE), ''),  # 更精确的匹配
        
        # 括号内容移除（保持原样，这个没问题）
        (re.compile(r'[（\(].*?[）\)]'), ''),  
        
        # 改进的短横线处理
        (re.compile(r'\s*-\s*'), ' '),  # 匹配任意数量空格环绕的短横线，替换为单个空格
    ]
    
    for pattern, repl in patterns:
        artist_name = pattern.sub(repl, artist_name)

    return artist_name.strip()

# 清洗歌曲名称，去除括号及其内容、与歌手名称相同的部分以及换行符和制表符
# 输入：字符串（未清洗的歌曲名称），字符串（未清洗的歌手名称）
# 输出：字符串（已清洗的歌曲名称）
def clean_song_name(song_name: str, artist_name: str):
    if not isinstance(song_name, str):
        song_name = str(song_name)

    patterns = [
        (re.compile(rf'{re.escape(artist_name)}'), ''),  # 去除歌手名
        (re.compile(r' - [（\(].*?[）\)]'), ''),        # 去除" - (内容)"
        (re.compile(r'[（\(].*?[）\)]'), ''),         # 去除"(内容)"
        (re.compile(r'\[.*?\]'), ''),                 # 去除"[内容]"
        (re.compile(r'[  ]ft[  .].*', re.IGNORECASE), ''),  # 去除ft/feat部分(不区分大小写)
        (re.compile(r'[-)）]'), ''),                   # 去除特殊字符
        (re.compile(r'[\t\n]'), '')                   # 去除空白字符
    ]

    # 应用所有正则替换
    for pattern, repl in patterns:
        song_name = pattern.sub(repl, song_name)
        
    return song_name.strip()

def main():
    # 读取文件夹路径
    folder_paths = [
        'QQ Music',
        'NetEase Music',
        'Kugou Music',
        'Apple Music'
    ]

    # 遍历文件夹并处理一个未读取的文件
    for folder in folder_paths:
        files = sorted(os.listdir(f'{os.getcwd()}/{folder}'))  # 按文件名顺序读取文件
        for file in files:
            if file.endswith('.xls') or file.endswith('.xlsx'): # 文件类型为 xls 或 xlsx
                # 设置当前文件的路径
                file_path = f'{folder}/{file}'
                print(file_path)

                # 读取sheet name
                excel_file = pd.ExcelFile(file_path)
                sheet_name = excel_file.sheet_names[0]

                # 读取数据
                df = pd.read_excel(file_path, usecols=[0, 1], names=['Song Name', 'Artist'])
                
                # 逐行清洗数据
                for index, row in df.iterrows():
                    df.at[index, 'Song Name'] = clean_song_name(row['Song Name'], row["Artist"]) # 清理歌曲名称
                    df.at[index, 'Artist'] = clean_artist_name(row['Artist']) # 清理歌手名称

                with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0, index=False)# 指定写入工作表、起始行和起始列

main()          