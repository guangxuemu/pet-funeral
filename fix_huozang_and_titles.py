#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复两个问题：
1. 将"宠物火葬"改为"宠物殡葬"或"宠物火化"
2. 统一城市页面title和H1标题
"""

import os
import glob
import re
from pathlib import Path

class ContentFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.stats = {
            'huozang_fixed': 0,
            'title_h1_fixed': 0,
            'files_checked': 0
        }
    
    def fix_huozang_in_file(self, file_path):
        '''修复文件中的"宠物火葬"为"宠物殡葬"或"宠物火化"'''
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 替换规则：
            # "宠物火葬" -> "宠物殡葬" (在服务/机构语境中)
            # "宠物火葬" -> "宠物火化" (在技术/流程语境中)
            # "单独宠物火葬" -> "单独宠物火化"
            # "宠物火葬场" -> "宠物火化中心"
            # "宠物火葬服务" -> "宠物殡葬服务"
            
            replacements = [
                (r'单独宠物火葬', '单独宠物火化'),
                (r'宠物火葬场', '宠物火化中心'),
                (r'宠物火葬服务', '宠物殡葬服务'),
                (r'宠物火葬机构', '宠物火化机构'),
                (r'宠物火葬中心', '宠物火化中心'),
                (r'专业宠物火葬', '专业宠物火化'),
                (r'进行宠物火葬', '进行宠物火化'),
                (r'提供宠物火葬', '提供宠物火化'),
                (r'宠物火葬价格', '宠物火化价格'),
                (r'宠物火葬费用', '宠物火化费用'),
                (r'宠物火葬多少钱', '宠物火化多少钱'),
                (r'有没有宠物火葬', '有没有宠物火化'),
                (r'附近宠物火葬', '附近宠物火化'),
                (r'上门宠物火葬', '上门宠物火化'),
                (r'正规宠物火葬', '正规宠物火化'),
                (r'本地宠物火葬', '本地宠物火化'),
                (r'宠物火葬的', '宠物火化的'),
                (r'([^临])宠物火葬', r'\1宠物火化'),  # 避免替换"临终"中的"临"
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # 最后处理单独的"宠物火葬"
            content = content.replace('宠物火葬', '宠物火化')
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.stats['huozang_fixed'] += 1
                return True
            return False
            
        except Exception as e:
            print(f"❌ 修复失败 {file_path}: {e}")
            return False
    
    def fix_title_h1_consistency(self, file_path, city_name):
        """修复title和H1不一致的问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 提取title
            title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            if not title_match:
                return False
            
            title = title_match.group(1).strip()
            
            # 提取H1（第一个#开头的行）
            h1_match = re.search(r'\n#\s*(.+?)(?:\n|$)', content)
            if not h1_match:
                return False
            
            h1 = h1_match.group(1).strip()
            
            # 检查是否一致（提取核心关键词部分）
            # title格式: "北京宠物火化服务|..."
            # H1格式: "# 北京宠物火化服务避坑指南..."
            
            # 提取title中的城市名+核心服务词
            title_core = re.search(r'([^|]+)', title)
            if not title_core:
                return False
            
            title_core = title_core.group(1).strip()
            
            # 检查H1是否包含title的核心部分
            # 如果不一致，修改H1以匹配title的核心
            
            # 获取title中的城市名
            city_in_title = re.search(r'^([^|]+?)(?:宠物|火化)', title)
            if city_in_title:
                city_from_title = city_in_title.group(1).strip()
                
                # 检查H1是否以城市名开头
                if not h1.startswith(city_from_title):
                    # 修改H1，使其与title一致
                    # 提取H1中的副标题部分
                    h1_subtitle = re.sub(r'^.*?宠物火化服务', '', h1)
                    if h1_subtitle:
                        new_h1 = f"{city_from_title}宠物火化服务{h1_subtitle}"
                    else:
                        new_h1 = f"{city_from_title}宠物火化服务 - 正规宠物火化机构"
                    
                    content = content.replace(f"# {h1}", f"# {new_h1}")
                    
                    if content != original:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        self.stats['title_h1_fixed'] += 1
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ 修复失败 {file_path}: {e}")
            return False
    
    def run_all_fixes(self):
        '''执行所有修复'''
        print("开始修复...\n")
        
        # 1. 修复所有文件中的"宠物火葬"
        print("[1/2] 修复'宠物火葬'用词...")
        md_files = glob.glob(str(self.base_dir / 'docs' / '**' / '*.md'), recursive=True)
        
        for file_path in md_files:
            self.stats['files_checked'] += 1
            if self.fix_huozang_in_file(file_path):
                print(f"✅ 已修复用词: {Path(file_path).name}")
        
        print(f"\n已检查 {self.stats['files_checked']} 个文件")
        print(f"已修复 {self.stats['huozang_fixed']} 个文件的用词\n")
        
        # 2. 修复城市页面title和H1一致性
        print("[2/2] 修复城市页面title和H1一致性...")
        city_files = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*' / '*' / 'index.md'))
        
        for file_path in city_files:
            city_name = Path(file_path).parent.name
            if self.fix_title_h1_consistency(file_path, city_name):
                print(f"✅ 已统一: {city_name}")
        
        self.print_report()
    
    def print_report(self):
        """打印报告"""
        print("\n" + "="*50)
        print("修复完成报告")
        print("="*50)
        print(f"检查文件数: {self.stats['files_checked']}")
        print(f"修复'火葬'用词: {self.stats['huozang_fixed']}")
        print(f"统一title/H1: {self.stats['title_h1_fixed']}")
        print("="*50)

if __name__ == "__main__":
    fixer = ContentFixer('/home/mz/.openclaw/workspace/pet-funeral')
    fixer.run_all_fixes()
