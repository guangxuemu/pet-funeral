#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有确认的问题
"""

import os
import re
from pathlib import Path

class IssueFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.stats = {
            'desc_fixed': 0,
            'link_fixed': 0,
            'title_h1_fixed': 0
        }
    
    def fix_description(self, file_path):
        """缩短description"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 查找description
            desc_match = re.search(r'^description:\s*(.+?)(?=\n\w|$)', content, re.MULTILINE | re.DOTALL)
            if not desc_match:
                return False
            
            desc = desc_match.group(1).strip()
            
            # 如果超过160字符，截取
            if len(desc) > 160:
                # 截取到150字符
                new_desc = desc[:150].rsplit('，', 1)[0].rsplit('。', 1)[0]
                if len(new_desc) < 100:
                    new_desc = desc[:150]
                new_desc = new_desc + '...'
                
                content = content.replace(f'description: {desc}', f'description: {new_desc}')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            return False
    
    def fix_dead_links(self, file_path):
        """修复404链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 修复不存在的链接
            content = re.sub(r'\[([^\]]+)\]\((/安放)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/安葬[^)]*)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/纪念[^)]*)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/寄存[^)]*)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/告别仪式)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/纪念品)\)', r'\1', content)
            content = re.sub(r'\[([^\]]+)\]\((/memorial)\)', r'\1', content)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            return False
    
    def fix_title_h1(self, file_path):
        """统一Title和H1"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 提取当前title
            title_match = re.search(r'^title:\s*([^\n]+)', content, re.MULTILINE)
            if not title_match:
                return False
            
            title = title_match.group(1).strip()
            
            # 提取H1
            h1_match = re.search(r'\n#\s*([^\n]+)\n', content)
            if not h1_match:
                return False
            
            h1 = h1_match.group(1).strip()
            
            # 统一：让title与H1保持一致
            h1_core = h1.split('：')[0] if '：' in h1 else h1
            title_core = title.split('|')[0] if '|' in title else title
            
            if h1_core != title_core and len(h1_core) > 5:
                new_title = f"{h1_core}|附近宠物火化|附近宠物殡葬 - 百情宠物善终"
                content = content.replace(f'title: {title}', f'title: {new_title}')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            return False
    
    def run(self):
        """执行所有修复"""
        print("开始修复所有确认的问题...\n")
        
        # 获取所有页面
        all_files = list(self.base_dir.glob('docs/**/*.md'))
        
        print(f"共 {len(all_files)} 个页面需要处理\n")
        
        for idx, file_path in enumerate(sorted(all_files)):
            if idx % 100 == 0 and idx > 0:
                print(f"  ... 已处理 {idx}/{len(all_files)}")
            
            if self.fix_description(file_path):
                self.stats['desc_fixed'] += 1
            
            if self.fix_dead_links(file_path):
                self.stats['link_fixed'] += 1
            
            if self.fix_title_h1(file_path):
                self.stats['title_h1_fixed'] += 1
        
        print("\n" + "="*60)
        print("修复完成报告")
        print("="*60)
        print(f"Description修复: {self.stats['desc_fixed']} 个页面")
        print(f"死链修复: {self.stats['link_fixed']} 个页面")
        print(f"Title/H1统一: {self.stats['title_h1_fixed']} 个页面")
        print("="*60)

if __name__ == "__main__":
    fixer = IssueFixer('/home/mz/.openclaw/workspace/pet-funeral')
    fixer.run()
