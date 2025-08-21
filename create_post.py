# create_post.py (v2 - 包含精確時間)
import os
import sys
import re
from datetime import datetime

# --- 設定區 ---
# 請將這裡的作者名改成您希望預設顯示的名字
DEFAULT_AUTHOR = "思无邪"
POSTS_DIRECTORY = "posts"


# --- 設定區結束 ---

def create_slug(title):
    """將文章標題轉換為 URL 友善的格式 (slug)"""
    slug = title.lower()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'[^\w\-\u4e00-\u9fff]', '', slug)
    return slug


def main():
    if len(sys.argv) < 2:
        print("❌ 使用方式錯誤！")
        print("   請提供文章標題作為參數。")
        print("   範例: python create_post.py 我美好的第一篇文章")
        sys.exit(1)

    post_title = " ".join(sys.argv[1:])

    # 【更新點】獲取今天的日期和時間 (例如 "2025-08-21 18:57")
    now_obj = datetime.now()
    date_str_for_folder = now_obj.strftime("%Y-%m-%d")
    datetime_str_for_yaml = now_obj.strftime("%Y-%m-%d %H:%M")

    post_slug = create_slug(post_title)

    # 資料夾名稱只使用日期，保持簡潔
    dir_name = f"{date_str_for_folder}-{post_slug}"
    full_dir_path = os.path.join(POSTS_DIRECTORY, dir_name)

    if not os.path.exists(POSTS_DIRECTORY):
        os.makedirs(POSTS_DIRECTORY)
        print(f"📁 已創建 '{POSTS_DIRECTORY}' 資料夾。")

    if os.path.exists(full_dir_path):
        print(f"❌ 錯誤：資料夾 '{full_dir_path}' 已經存在。")
        sys.exit(1)

    os.makedirs(full_dir_path)

    # 【更新點】準備包含精確時間的 index.qmd 內容
    qmd_content = f'''---
title: "{post_title}"
author: "{DEFAULT_AUTHOR}"
date: "{datetime_str_for_yaml}"
categories: []
---

在這裡開始寫您的正文...
'''

    qmd_file_path = os.path.join(full_dir_path, "index.qmd")
    with open(qmd_file_path, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    print("✅ 成功創建文章！")
    print(f"   檔案位於: {qmd_file_path}")


if __name__ == "__main__":
    main()