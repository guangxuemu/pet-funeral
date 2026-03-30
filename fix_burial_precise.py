#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复：只修复真正把土葬作为服务选项的文件
"""
import os
import re

# 精确匹配规则：真正把土葬作为选项的表述
PATTERNS_TO_FIX = [
    # 1. 明确把土葬作为选项
    {
        'pattern': r'只能选择土葬',
        'replacement': '需要专业火化服务',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬与生态安葬选项',
        'replacement': '生态纪念安置方案',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'提供土葬服务',
        'replacement': '提供专业火化服务',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'可以选择土葬',
        'replacement': '可以选择专业火化后的纪念安置',
        'desc': '引导火化'
    },
    {
        'pattern': r'可选择土葬',
        'replacement': '可选择专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'支持土葬',
        'replacement': '支持专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'可以土葬',
        'replacement': '可以选择其他纪念方式',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'能土葬',
        'replacement': '能选择其他纪念方式',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'还提供了土葬',
        'replacement': '还提供了多种纪念安置方案',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'我们也提供土葬',
        'replacement': '我们也提供多种纪念安置方案',
        'desc': '删除土葬选项'
    },
    
    # 2. FAQ中把土葬作为选项
    {
        'pattern': r'Q：是否必须火化\?可以土葬吗\?',
        'replacement': 'Q：为什么要选择火化而不是土葬？',
        'desc': '修改FAQ'
    },
    {
        'pattern': r'Q：是否必须火化\?是否可以土葬\?',
        'replacement': 'Q：为什么要选择火化而不是土葬？',
        'desc': '修改FAQ'
    },
    {
        'pattern': r'Q：有没有土葬选项',
        'replacement': 'Q：有哪些纪念方式可以选择',
        'desc': '修改FAQ'
    },
    {
        'pattern': r'Q：可以土葬吗',
        'replacement': 'Q：为什么要选择专业火化服务',
        'desc': '修改FAQ'
    },
    {
        'pattern': r'Q：能土葬吗',
        'replacement': 'Q：有哪些纪念方式',
        'desc': '修改FAQ'
    },
    
    # 3. 服务流程中的土葬选项
    {
        'pattern': r'火化、土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬或火化',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化或土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬/火化',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化/土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    
    # 4. 协助/办理土葬
    {
        'pattern': r'协助办理土葬',
        'replacement': '协助办理火化后的纪念安置',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'可协助.*?土葬',
        'replacement': '可协助骨灰纪念安置',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'办理土葬',
        'replacement': '办理火化后的纪念安置',
        'desc': '删除土葬服务'
    },
    
    # 5. 其他明确选项
    {
        'pattern': r'土葬方案',
        'replacement': '纪念安置方案',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬服务',
        'replacement': '纪念安置服务',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'生态土葬',
        'replacement': '生态纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'家庭土葬',
        'replacement': '家庭纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'私人土葬',
        'replacement': '私人纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'若您选择土葬',
        'replacement': '若您选择火化后的纪念安置',
        'desc': '引导火化'
    },
    {
        'pattern': r'如需土葬',
        'replacement': '如需了解其他方式',
        'desc': '删除土葬引导'
    },
    {
        'pattern': r'坚持土葬',
        'replacement': '考虑其他方式',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'倾向土葬',
        'replacement': '倾向纪念安置',
        'desc': '删除土葬表述'
    },
]

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for rule in PATTERNS_TO_FIX:
        if re.search(rule['pattern'], content):
            content = re.sub(rule['pattern'], rule['replacement'], content)
            changes.append(rule['desc'])
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

def main():
    base_dir = "/home/mz/.openclaw/workspace/pet-funeral/docs/cities"
    fixed_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fixed, changes = fix_file(filepath)
                if fixed:
                    rel_path = filepath.replace(base_dir, '').lstrip('/')
                    fixed_files.append({
                        'file': rel_path,
                        'changes': changes
                    })
    
    print("=" * 80)
    print("土葬选项精确修复报告")
    print("=" * 80)
    print(f"\n共修复 {len(fixed_files)} 个文件\n")
    
    for item in fixed_files:
        print(f"📄 {item['file']}")
        for change in item['changes']:
            print(f"   ✓ {change}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
