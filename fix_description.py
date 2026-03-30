#!/usr/bin/env python3
"""
批量修复description中的问题：
1. 删除"、等服务"
2. 删除"、,"等多余标点
3. 添加骨灰处理说明
"""

import re
from pathlib import Path

def fix_description(content):
    """修复description"""
    # 修复"、等服务"或",等服务"
    content = re.sub(r'[、,，]等服务', '服务', content)
    content = re.sub(r'[、,，]等。', '。', content)
    # 修复连续标点
    content = re.sub(r'[、,，]{2,}', '、', content)
    # 修复"滨海城市"+海葬相关内容删除后的残留
    content = re.sub(r'，[^。]*我们提供[^。]*服务[^。]*', '，我们提供专业火化服务', content)
    # 添加骨灰处理说明（如果没有）
    if '骨灰' not in content and '自行' not in content:
        content = re.sub(r'(咨询微信\d+)', r'火化完成后骨灰由主人自行带走处理。\1', content)
    return content

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_description(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    docs_dir = Path('/home/mz/.openclaw/workspace/pet-funeral/docs/cities')
    md_files = list(docs_dir.rglob('*.md'))
    
    modified = 0
    for filepath in md_files:
        if process_file(filepath):
            modified += 1
    
    print(f"Modified: {modified} files")

if __name__ == '__main__':
    main()
