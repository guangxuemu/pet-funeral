#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理城市页面中H1标题上方的多余内容
删除出现在frontmatter之后、H1之前的重复介绍文字
"""

import os
import glob
import re
from pathlib import Path

class ExcessContentCleaner:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.stats = {
            'checked': 0,
            'cleaned': 0
        }
    
    def clean_file(self, file_path):
        """清理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 匹配模式：frontmatter结束后、H1之前的多余内容
            # 删除形如："XX宠物XX服务由百情宠物善终提供专业支持。XXX" 的段落
            pattern = r'(---\n+)([^#\n]*?宠物(?:火化|殡葬|告别|善终)[^#\n]*?由百情宠物善终提供[^#\n]*?\n+)(#[^#])'
            
            # 替换为直接保留frontmatter和H1，删除中间的内容
            content = re.sub(pattern, r'\1\3', content)
            
            # 再处理一次，确保清理干净
            # 删除以"由百情宠物善终提供专业支持"结尾的段落
            pattern2 = r'(---\n+)([^#\n]*?由百情宠物善终提供[^#\n]*?\n+)(#[^#])'
            content = re.sub(pattern2, r'\1\3', content)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            print(f"❌ 清理失败 {file_path}: {e}")
            return False
    
    def run(self):
        """执行清理"""
        print("开始清理多余内容...\n")
        
        # 清理城市页面
        city_files = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*' / '*' / 'index.md'))
        
        for file_path in sorted(city_files):
            city_name = Path(file_path).parent.name
            self.stats['checked'] += 1
            
            if self.clean_file(file_path):
                print(f"✅ 已清理: {city_name}")
                self.stats['cleaned'] += 1
        
        print(f"\n{'='*50}")
        print(f"检查文件数: {self.stats['checked']}")
        print(f"清理文件数: {self.stats['cleaned']}")
        print(f"{'='*50}")

if __name__ == "__main__":
    cleaner = ExcessContentCleaner('/home/mz/.openclaw/workspace/pet-funeral')
    cleaner.run()
