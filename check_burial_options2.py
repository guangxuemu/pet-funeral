#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查是否还有土葬作为选项的表述
"""
import os
import re

# 检查是否把土葬作为服务选项
BURIAL_OPTION_PATTERNS = [
    r'提供.*?土葬',
    r'可选.*?土葬',
    r'选择.*?土葬',
    r'土葬.*?选项',
    r'可以.*?土葬',
    r'火化.*?或.*?土葬',
    r'土葬.*?或.*?火化',
]

def check_file(filepath):
    """检查单个文件"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # 跳过劝退土葬的语境
        if any(w in line for w in ['不建议', '避免', '隐患', '风险', '禁止', '不推荐', '受限于', '可能违反', '逐渐退出', '不推荐']):
            continue
        
        # 跳过解释为什么不选土葬的语境
        if '相比土葬' in line or '相比' in line and '土葬' in line:
            continue
        
        for pattern in BURIAL_OPTION_PATTERNS:
            if re.search(pattern, line):
                issues.append({
                    'line': line_num,
                    'content': line.strip()
                })
                break
    
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
    print("土葬选项检查报告（修复后）")
    print("=" * 70)
    
    if not all_issues:
        print("\n✅ 未发现把土葬作为服务选项的表述！")
        return
    
    print(f"\n发现 {len(all_issues)} 个文件仍有问题：\n")
    
    for item in all_issues[:20]:
        print(f"📄 {item['file']}")
        for issue in item['issues']:
            print(f"   第{issue['line']}行: {issue['content'][:70]}...")
        print()

if __name__ == "__main__":
    main()
