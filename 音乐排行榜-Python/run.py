import subprocess
import sys

def run_script(script_name: str, task_name: str) -> bool:
    try:
        subprocess.run(
            [sys.executable, script_name],
            capture_output=True,      # 捕获标准输出和错误
            text=True,                # 以文本形式返回
            check=True )
        return True
    except Exception as e:
        print(f'执行{task_name}时发生意外：{e}')
        return False
    finally:
        print(f"{task_name}已完成")

def main():
    scripts = [
        ("Music_website_capture.py", "数据抓取"),
        ("Data_Clean.py", "数据清洗"),
        ("Generate_Html.py", "生成排行榜")
    ]

    for script, task in scripts:
        result = run_script(script, task)
        if not result:
            print(f"{task}执行失败")
            sys.exit(1)

    print("所有任务已完成")

if __name__ == "__main__":
    main()