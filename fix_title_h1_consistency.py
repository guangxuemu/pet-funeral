#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一城市页面的title和H1标题
使H1与title的核心内容保持一致
"""

import os
import glob
import re
from pathlib import Path

class TitleH1Unifier:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.stats = {
            'checked': 0,
            'fixed': 0
        }
    
    def unify_file(self, file_path, city_name):
        """统一单个文件的title和H1"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 提取title中的核心部分（城市名+服务）
            title_match = re.search(r'^title:\s*([^|]+)', content, re.MULTILINE)
            if not title_match:
                return False
            
            title_core = title_match.group(1).strip()
            # 移除 " - 百情宠物善终" 后缀
            title_core = re.sub(r'\s+-\s+百情宠物善终$', '', title_core)
            
            # 构造统一的H1
            new_h1 = f"# {title_core}"
            
            # 替换现有的H1
            content = re.sub(r'\n#\s*.+?\n', f'\n{new_h1}\n', content, count=1)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            print(f"❌ 修复失败 {file_path}: {e}")
            return False
    
    def run(self):
        """执行统一"""
        print("开始统一title和H1...\n")
        
        # 处理城市页面
        city_files = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*' / '*' / 'index.md'))
        
        for file_path in sorted(city_files):
            city_name = Path(file_path).parent.name
            self.stats['checked'] += 1
            
            if self.unify_file(file_path, city_name):
                print(f"✅ 已统一: {city_name}")
                self.stats['fixed'] += 1
        
        print(f"\n{'='*50}")
        print(f"检查文件数: {self.stats['checked']}")
        print(f"修复文件数: {self.stats['fixed']}")
        print(f"{'='*50}")

if __name__ == "__main__":
    unifier = TitleH1Unifier('/home/mz/.openclaw/workspace/pet-funeral')
    unifier.run()
