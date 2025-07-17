import os
import pandas as pd
from datetime import datetime

# 合并 Excel文件数据
# 输入：列表（读取文件夹内文件的顺序），列表（各网站文件夹的路径）
# 输出：字典（按权重排序的整合数据）
def merge_com_excel(sheet_names, folder_paths):
    # 创建整合字典，name作为键，三列的dataframe作为值
    com_data = {name: pd.DataFrame(columns=['Song Name', 'Artist', 'Weight']) for name in sheet_names}

    for folder in folder_paths:
        for i, file in enumerate(sorted(os.listdir(f'{os.getcwd()}/{folder}'))):
            sheet_idx = i % 3
            # 读取和处理文件内容
            file_path = os.path.join(folder, file)
            data = pd.read_excel(file_path) #当前路径位于文件夹外，需要获取excel文件路径并读取内容
            data.loc[0:16,'Weight'] = range(17,0,-1)

            # 合并数据
            current_sheet = com_data[sheet_names[sheet_idx]] # 合并字典中的单个表
            merged = pd.merge(current_sheet, data, on=['Song Name', 'Artist'], how='inner')

            # 更新权重
            for _, row in merged.iterrows():
                com_data[sheet_names[sheet_idx]].loc[com_data[sheet_names[sheet_idx]]['Song Name'] == row['Song Name'],"Weight"] = row['Weight_x']
            
            # 合并并去重
            com_data[sheet_names[sheet_idx]] = pd.concat([current_sheet, data]) \
                    .sort_values('Weight', ascending=False) \
                    .drop_duplicates(['Song Name', 'Artist'])
    return com_data

# 生成 HTML 文件
# 输入：列表（读取文件夹内文件的顺序），字符串（Excel文件的路径），字符串（html文件预定的保存路径）
# 输出：无
def generate_html(sheet_names, output_xls_file, output_html_file):
    xls = pd.ExcelFile(output_xls_file)

    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write('<html><head><meta charset="utf-8"><title>音乐排行榜('+str(datetime.now().date())+')</title></head><body>\n')

        for sheet_name in sheet_names:
            f.write(f'<h2>{sheet_name}</h2>\n')
            df = pd.read_excel(xls, sheet_name=sheet_name)

            f.write('<table border="1">\n<tr><th>Song Name</th><th>Artist</th></tr>\n')
            for _, row in df.head(20).iterrows():
                f.write(f'<tr><td>{row["Song Name"]}</td><td>{row["Artist"]}</td></tr>\n')
            f.write('</table>\n')

        f.write('</body></html>')
    return

def main():
    folder_paths = [ # 定义文件夹路径
        'QQ Music',
        'NetEase Music',
        'Kugou Music',
        'Apple Music'
    ]
    sheet_names = ['飙升榜', '热歌榜', '新歌榜'] # 表单名称
    output_xls_file = 'Combine/consolidated_music_data.xlsx' # 合并Excel文件的路径
    output_html_file = 'html/music_rankings.html' # HTML文件预定的保存路径
    if not os.path.exists("Combine"): # 创建Combine文件夹保存合并Excel文件
        os.mkdir("Combine")
    if not os.path.exists('html'):
        os.mkdir('html')

    # 合并 Excel文件数据 与 合并字典
    com_data = merge_com_excel(sheet_names, folder_paths)

    # 将 合并字典 写入新Excel文件
    with pd.ExcelWriter(output_xls_file, engine='openpyxl') as writer:
        for sheet_name in sheet_names:
            sorted_data = com_data[sheet_name].sort_values(by='Weight', ascending=False)
            sorted_data.to_excel(writer, sheet_name=sheet_name, index=False)

    # 调用合并Excel文件，生成 HTML 文件
    generate_html(sheet_names, output_xls_file, output_html_file)

    # 整合结束
    print("所有音乐数据已成功整合并保存，HTML 文件也已生成。"+str(datetime.now().date()))
    return 

main()