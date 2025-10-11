# create_post.py (v3 - 优化版)
import os
import sys
import re
from datetime import datetime

# --- 配置区 ---
DEFAULT_AUTHOR = "思无邪"
POSTS_DIRECTORY = "posts"
# --- 配置区结束 ---

def create_slug(title):
    """将文章标题转换为 URL 友善的格式 (slug)，更健壮"""
    # 移除 YAML 中可能存在的引号
    title = title.strip().strip("'\"")
    slug = title.lower()
    # 将空格替换为连字符
    slug = re.sub(r'\s+', '-', slug)
    # 只保留字母、数字、连字符和中文字符
    slug = re.sub(r'[^\w\-\u4e00-\u9fff]', '', slug)
    # 避免多个连字符连在一起
    slug = re.sub(r'--+', '-', slug)
    # 避免过长的文件名，截取前80个字符
    return slug.strip('-')[:80]

def main():
    """主函数，用于创建新的文章文件夹和 index.qmd"""
    if len(sys.argv) < 2:
        print("❌ 使用方式错误！")
        print("   请提供文章标题作为参数。")
        print("   范例: python create_post.py 我美好的第一篇文章")
        sys.exit(1)

    post_title = " ".join(sys.argv[1:])

    # 获取当前精确日期和时间
    now_obj = datetime.now()
    # 文件夹名称只使用日期，格式 YYYY-MM-DD
    date_str_for_folder = now_obj.strftime("%Y-%m-%d")
    # YAML元数据中的日期包含时和分，格式 YYYY-MM-DD HH:MM
    datetime_str_for_yaml = now_obj.strftime("%Y-%m-%d %H:%M")

    # 根据标题生成 URL 友善的 slug
    post_slug = create_slug(post_title)

    # 组合成最终的文件夹名
    dir_name = f"{date_str_for_folder}-{post_slug}"
    full_dir_path = os.path.join(POSTS_DIRECTORY, dir_name)

    # 检查 posts 文件夹是否存在，不存在则创建
    if not os.path.exists(POSTS_DIRECTORY):
        os.makedirs(POSTS_DIRECTORY)
        print(f"📁 已创建 '{POSTS_DIRECTORY}' 資料夾。")

    # 检查目标文章文件夹是否已存在，避免重复
    if os.path.exists(full_dir_path):
        print(f"❌ 错误：資料夾 '{full_dir_path}' 已经存在。")
        sys.exit(1)

    # 创建文章文件夹
    os.makedirs(full_dir_path)

    # 准备 index.qmd 的内容模板
    qmd_content = f'''---
title: "{post_title}"
author: "{DEFAULT_AUTHOR}"
date: "{datetime_str_for_yaml}"
categories: []
---

在这里开始写您的正文...
'''

    # 写入 index.qmd 文件
    qmd_file_path = os.path.join(full_dir_path, "index.qmd")
    with open(qmd_file_path, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    print("✅ 成功創建文章！")
    print(f"   文章位於: {qmd_file_path}")

if __name__ == "__main__":
    main()