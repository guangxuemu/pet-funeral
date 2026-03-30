#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查是否有鼓励/引导土葬的内容，确保全面引导火化
"""
import os
import re

# 可能暗示土葬的词汇或表述
BURIAL_KEYWORDS = [
    '土葬', '埋葬', '掩埋', '深埋', '入土为安', '落叶归根',
    '挖坑', '埋在后院', '埋在花园', '自行处理', '自己埋'
]

# 需要重点检查的表述
PROBLEMATIC_PATTERNS = [
    r'可以选择.*埋葬',
    r'可以.*自行.*[埋|葬]',
    r'建议.*[埋|葬]',
    r'允许.*[埋|葬]',
]

def check_file(filepath):
    """检查单个文件"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # 检查是否在劝退土葬的语境中
        is_warning_context = any(w in line for w in ['隐患', '风险', '不建议', '禁止', '不能', '避免'])
        
        for keyword in BURIAL_KEYWORDS:
            if keyword in line:
                # 如果不是劝退语境，标记为问题
                if not is_warning_context and not any(w in line for w in ['不建议', '避免', '隐患', '风险', '禁止']):
                    issues.append({
                        'line': line_num,
                        'keyword': keyword,
                        'content': line.strip(),
                        'context': 'warning' if is_warning_context else 'neutral'
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
    
    print("=" * 70)
    print("土葬相关内容检查报告")
    print("=" * 70)
    
    if not all_issues:
        print("\n✅ 未发现可能引导土葬的表述！")
        return
    
    print(f"\n发现 {len(all_issues)} 个文件需要关注：\n")
    
    for item in all_issues[:20]:  # 只显示前20个
        print(f"📄 {item['file']}")
        for issue in item['issues']:
            status = "⚠️" if issue['context'] == 'neutral' else "✓"
            print(f"   {status} 第{issue['line']}行 [{issue['keyword']}]: {issue['content'][:70]}...")
        print()
    
    if len(all_issues) > 20:
        print(f"... 还有 {len(all_issues) - 20} 个文件未显示")

if __name__ == "__main__":
    main()
