#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有确认的问题：
1. Description过长（缩短至160字符以内）
2. 404链接（删除或修复）
3. Title/H1不一致（统一格式）
"""

import os
import re
import glob
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
        """缩短description至160字符以内"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 查找description
            desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
            if not desc_match:
                return False
            
            desc = desc_match.group(1).strip()
            
            # 如果超过160字符，截取并添加省略号
            if len(desc) > 160:
                # 截取到150字符，避免截断在单词中间
                new_desc = desc[:150].rsplit(' ', 1)[0] + '...'
                content = content.replace(f'description: {desc}', f'description: {new_desc}')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Description修复失败 {file_path}: {e}")
            return False
    
    def fix_dead_links(self, file_path):
        """修复404链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 修复各种不存在的链接
            # 1. 移除指向不存在的页面的链接，保留文本
            replacements = [
                (r'\[([^\]]+)\]\((/安放)\)', r'\1'),
                (r'\[([^\]]+)\]\((/安葬)\)', r'\1'),
                (r'\[([^\]]+)\]\((/纪念)\)', r'\1'),
                (r'\[([^\]]+)\]\((/寄存)\)', r'\1'),
                (r'\[([^\]]+)\]\((/告别仪式)\)', r'\1'),
                (r'\[([^\]]+)\]\((/纪念品)\)', r'\1'),
                (r'\[([^\]]+)\]\((/memorial[^)]*)\)', r'\1'),
                (r'\[([^\]]+)\]\((/services[^)]*)\)', r'\1'),
                (r'\[([^\]]+)\]\((/faq[^)]*)\)', r'\1'),
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # 2. 修复格式错误的链接（如 /安徽/ → /cities/安徽/）
            content = re.sub(r'\[([^\]]+)\]\((/安徽/[^)]*)\)', r'[\1](/cities\2)', content)
            content = re.sub(r'\[([^\]]+)\]\((/广东/[^)]*)\)', r'[\1](/cities\2)', content)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            print(f"❌ 链接修复失败 {file_path}: {e}")
            return False
    
    def fix_title_h1(self, file_path, city_name):
        """统一Title和H1"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 提取H1
            h1_match = re.search(r'\n#\s*([^\n]+)\n', content)
            if not h1_match:
                return False
            
            h1 = h1_match.group(1).strip()
            
            # 提取H1核心部分（冒号前的内容）
            h1_core = h1.split('：')[0] if '：' in h1 else h1
            h1_core = h1_core.split(' ')[0] if ' ' in h1_core else h1_core
            
            # 更新title，使其与H1核心一致
            new_title = f"{h1_core}|附近宠物火化|附近宠物殡葬 - 百情宠物善终"
            content = re.sub(r'^title:\s*[^\n]+', f'title: {new_title}', content, flags=re.MULTILINE)
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Title/H1修复失败 {file_path}: {e}")
            return False
    
    def run(self):
        """执行所有修复"""
        print("开始修复所有确认的问题...\n")
        
        # 获取所有城市页面
        city_files = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*' / '*' / 'index.md'))
        
        print(f"共 {len(city_files)} 个城市页面需要处理\n")
        
        for idx, file_path in enumerate(sorted(city_files)):
            city_name = Path(file_path).parent.name
            
            # 每50个显示进度
            if idx % 50 == 0 and idx > 0:
                print(f"  ... 已处理 {idx}/{len(city_files)}")
            
            # 1. 修复description
            if self.fix_description(file_path):
                self.stats['desc_fixed'] += 1
            
            # 2. 修复死链
            if self.fix_dead_links(file_path):
                self.stats['link_fixed'] += 1
            
            # 3. 统一title和H1
            if self.fix_title_h1(file_path, city_name):
                self.stats['title_h1_fixed'] += 1
        
        # 打印报告
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
