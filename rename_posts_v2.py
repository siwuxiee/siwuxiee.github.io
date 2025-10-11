# rename_posts_v2.py (qmd-centric version)
import os
import re
import sys
from datetime import datetime

# --- 配置区 ---
POSTS_DIRECTORY = "posts"
# --- 配置区结束 ---

def create_slug(title):
    """将文章标题转换为 URL 友善的格式 (slug)"""
    title = title.strip().strip("'\"")
    slug = title.lower()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'[^\w\-\u4e00-\u9fff]', '', slug)
    slug = re.sub(r'--+', '-', slug)
    return slug.strip('-')[:80]

def get_metadata_from_qmd(folder_path):
    """从文件夹内的 .qmd 文件中读取 title 和 date"""
    qmd_path = os.path.join(folder_path, "index.qmd")
    if not os.path.exists(qmd_path):
        try:
            first_qmd = next(f for f in os.listdir(folder_path) if f.endswith('.qmd'))
            qmd_path = os.path.join(folder_path, first_qmd)
        except (StopIteration, FileNotFoundError):
            return None # 没找到任何 .qmd 文件

    metadata = {}
    try:
        with open(qmd_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 简单地用正则表达式提取，足以应对大多数情况
            title_match = re.search(r'^title:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
            date_match = re.search(r'^date:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)

            if title_match:
                metadata['title'] = title_match.group(1).strip()
            if date_match:
                metadata['date'] = date_match.group(1).strip()
            
            return metadata if 'title' in metadata and 'date' in metadata else None

    except Exception:
        return None

def main():
    """主函数，执行基于QMD元数据的重命名逻辑"""
    is_dry_run = "--execute" not in sys.argv
    
    if is_dry_run:
        print("💧 正在以安全模式（Dry Run）运行。将只读取QMD元数据并显示计划。")
        print("   若要实际执行重命名，请使用命令: python rename_posts_v2.py --execute\n")
    else:
        print("🚀 警告：正在以执行模式运行，将根据QMD元数据实际重命名文件夹。\n")

    if not os.path.exists(POSTS_DIRECTORY):
        print(f"❌ 错误：找不到 '{POSTS_DIRECTORY}' 文件夹。")
        return

    rename_plan = []

    # 1. 收集所有计划
    for folder_name in sorted(os.listdir(POSTS_DIRECTORY)):
        original_path = os.path.join(POSTS_DIRECTORY, folder_name)
        if not os.path.isdir(original_path):
            continue

        metadata = get_metadata_from_qmd(original_path)
        
        if not metadata:
            print(f"⚠️  警告: 在 '{folder_name}' 中找不到有效的 .qmd 文件或元数据，已跳过。")
            print("-" * 20)
            continue
        
        try:
            # 解析日期，即使它包含时间 "YYYY-MM-DD HH:MM"
            date_str_full = metadata['date']
            # 我们只取前10个字符 "YYYY-MM-DD"
            date_str_formatted = date_str_full[:10]
            # 验证一下日期格式是否正确
            datetime.strptime(date_str_formatted, "%Y-%m-%d")
        except (ValueError, IndexError):
            print(f"⚠️  警告: 在 '{folder_name}' 中发现无效的日期格式 '{metadata.get('date')}'，已跳过。")
            print("-" * 20)
            continue

        title = metadata['title']
        slug = create_slug(title)
        new_name = f"{date_str_formatted}-{slug}"
        
        if new_name != folder_name:
             rename_plan.append({'old': folder_name, 'new': new_name})

    # 2. 显示并执行计划
    if not rename_plan:
        print("🎉 所有文件夹命名已规范，无需操作！")
        return

    print("以下是重命名计划：\n")
    for plan in rename_plan:
        print(f"📁 {plan['old']}")
        print(f"   ➡️  {plan['new']}\n")

    if not is_dry_run:
        user_input = input("您确定要执行以上所有重命名吗？ (y/n): ")
        if user_input.lower() == 'y':
            print("\n🚀 开始执行重命名...")
            for plan in rename_plan:
                original_path = os.path.join(POSTS_DIRECTORY, plan['old'])
                new_path = os.path.join(POSTS_DIRECTORY, plan['new'])
                
                if os.path.exists(new_path):
                     print(f"⚠️  跳过: 目标 '{plan['new']}' 已存在。")
                     continue
                try:
                    os.rename(original_path, new_path)
                    print(f"✅ 已重命名: {plan['old']} -> {plan['new']}")
                except OSError as e:
                    print(f"❌ 失败: {plan['old']} ({e})")
            print("\n✨ 整理完成！")
        else:
            print("\n操作已取消。")

if __name__ == "__main__":
    main()