#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有过长的description
"""

import os
import re
from pathlib import Path

def fix_description_file(file_path):
    """修复单个文件的description"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 查找description
        desc_match = re.search(r'^description:\s*(.+?)(?=\n\w|$)', content, re.MULTILINE | re.DOTALL)
        if not desc_match:
            return False
        
        desc = desc_match.group(1).strip()
        
        # 如果超过160字符，智能截取
        if len(desc) > 160:
            # 提取城市名
            city_match = re.search(r'^title:\s*([^|\n]+)', content, re.MULTILINE)
            city_name = ""
            if city_match:
                city_name = city_match.group(1).strip().replace('宠物火化服务', '').replace(' ', '')[:10]
            
            # 智能截取原description
            new_desc = desc[:150].rsplit('。', 1)[0].rsplit('，', 1)[0]
            if len(new_desc) < 80:
                new_desc = desc[:150]
            new_desc = new_desc + '。微信923160208'
            
            content = content.replace(f'description: {desc}', f'description: {new_desc}')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"❌ 失败 {file_path}: {e}")
        return False

def main():
    base_dir = Path('/home/mz/.openclaw/workspace/pet-funeral')
    all_files = list(base_dir.glob('docs/**/*.md'))
    
    print(f"🤖 开始批量修复description... 共 {len(all_files)} 个文件\n")
    
    fixed_count = 0
    
    for idx, file_path in enumerate(sorted(all_files)):
        if idx % 500 == 0 and idx > 0:
            print(f"  进度: {idx}/{len(all_files)}")
        
        if fix_description_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ 修复完成！共修复 {fixed_count} 个页面的description")

if __name__ == "__main__":
    main()
