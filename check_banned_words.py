#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查禁用词"""
import os
import re

BANNED_WORDS = ['墓地', '安葬场', '安葬地', '陵园', '墓园', '公墓', '纪念园', '骨灰堂', '坟']

def check_file(filepath):
    """检查单个文件"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # 排除潞王坟乡和陵园路（真实地名）
        if '潞王坟乡' in line or '陵园路' in line:
            continue
        
        for word in BANNED_WORDS:
            if word in line:
                issues.append({
                    'line': line_num,
                    'word': word,
                    'content': line.strip()
                })
    
    return issues

def main():
    base_dir = "/home/mz/.openclaw/workspace/pet-funeral/docs/cities"
    all_issues = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                issues = check_file(filepath)
                if issues:
                    rel_path = filepath.replace(base_dir, '').lstrip('/')
                    all_issues.append({
                        'file': rel_path,
                        'issues': issues
                    })
    
    print("=" * 60)
    print("禁用词检查结果")
    print("=" * 60)
    
    if not all_issues:
        print("\n✅ 未发现禁用词！")
        return
    
    print(f"\n发现 {len(all_issues)} 个文件包含禁用词：\n")
    
    for item in all_issues:
        print(f"📄 {item['file']}")
        for issue in item['issues']:
            print(f"   第{issue['line']}行 [{issue['word']}]: {issue['content'][:60]}...")
        print()

if __name__ == "__main__":
    main()
