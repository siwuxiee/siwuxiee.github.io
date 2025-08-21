# create_post.py
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
    # 轉換為小寫
    slug = title.lower()
    # 將空格替換為連字號
    slug = re.sub(r'\s+', '-', slug)
    # 移除所有非 (英文、數字、連字號、中文字元) 的字元
    # 這個正則表達式保留了 CJK (中日韓) 字元
    slug = re.sub(r'[^\w\-\u4e00-\u9fff]', '', slug)
    return slug

def main():
    # 檢查是否提供了文章標題
    if len(sys.argv) < 2:
        print("❌ 使用方式錯誤！")
        print("   請提供文章標題作為參數。")
        print("   範例: python create_post.py 我美好的第一篇文章")
        sys.exit(1)

    # 從指令行參數獲取文章標題
    post_title = " ".join(sys.argv[1:])
    
    # 獲取今天的日期
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 生成 slug
    post_slug = create_slug(post_title)
    
    # 組合資料夾名稱
    dir_name = f"{today_str}-{post_slug}"
    full_dir_path = os.path.join(POSTS_DIRECTORY, dir_name)
    
    # 檢查 posts 資料夾是否存在，不存在則創建
    if not os.path.exists(POSTS_DIRECTORY):
        os.makedirs(POSTS_DIRECTORY)
        print(f"📁 已創建 '{POSTS_DIRECTORY}' 資料夾。")

    # 檢查文章資料夾是否已存在
    if os.path.exists(full_dir_path):
        print(f"❌ 錯誤：資料夾 '{full_dir_path}' 已經存在。")
        sys.exit(1)
        
    # 創建文章資料夾
    os.makedirs(full_dir_path)
    
    # 準備 index.qmd 的內容
    qmd_content = f'''---
title: "{post_title}"
author: "{DEFAULT_AUTHOR}"
date: "{today_str}"
categories: []
---

在這裡開始寫您的正文...
'''
    
    # 創建並寫入 index.qmd 檔案
    qmd_file_path = os.path.join(full_dir_path, "index.qmd")
    with open(qmd_file_path, 'w', encoding='utf-8') as f:
        f.write(qmd_content)
        
    print("✅ 成功創建文章！")
    print(f"   檔案位於: {qmd_file_path}")

if __name__ == "__main__":
    main()