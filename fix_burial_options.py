#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复把土葬作为选项的表述，确保引导客户选择火化
"""
import os
import re

# 需要修复的模式和替换方案
REPLACE_PATTERNS = [
    # 把土葬作为选项的FAQ回答
    {
        'pattern': r'A：是的，除传统土葬外，我们还提供.*?等选项',
        'replacement': 'A：我们主要提供专业火化服务，火化后的骨灰可选择寄存于纪念场所、制作纪念品或生态树葬等多种纪念方式。',
        'desc': '删除土葬作为选项的表述'
    },
    {
        'pattern': r'A：您可以选择火化、土葬.*?或集中处理',
        'replacement': 'A：我们推荐选择专业火化服务，这是最环保、安全且符合法规的处理方式。火化后的骨灰可选择多种纪念安置方式。',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'A：是的，我们也提供宠物土葬选项.*?',
        'replacement': 'A：我们主要提供专业火化服务。相比土葬，火化更安全卫生、环保合规，也更便于纪念安置。',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'根据您的需求选择土葬、海葬或树葬',
        'replacement': '根据您的需求选择骨灰寄存、纪念品定制或生态纪念安置',
        'desc': '删除土葬/海葬选项'
    },
    {
        'pattern': r'可选土葬、树葬或骨灰寄存',
        'replacement': '可选骨灰寄存、树葬纪念或纪念品定制',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'提供生态土葬或树木纪念安葬服务',
        'replacement': '提供生态纪念树葬或骨灰寄存服务',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'协助寻找合规的生态安葬点',
        'replacement': '协助联系合规的骨灰寄存场所或纪念安置点',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'我们也提供符合国家规范的环保土葬指导',
        'replacement': '我们确保火化服务符合国家环保规范',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'无论您选择火化、土葬或其他方式',
        'replacement': '无论您选择单独火化或集体火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'除了火化，我们还提供土葬服务',
        'replacement': '我们专注于提供专业火化服务',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'您可以选择将骨灰带回.*?或选择.*?进行土葬',
        'replacement': '您可以选择将骨灰带回供奉在家中，或寄存于我们的纪念场所',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'有没有土葬选项',
        'replacement': '有没有其他纪念方式',
        'desc': '修改问题'
    },
    {
        'pattern': r'专业火化/土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'可以选择土葬',
        'replacement': '建议选择专业火化服务',
        'desc': '引导火化'
    },
    {
        'pattern': r'可以选择.*?土葬',
        'replacement': '建议选择专业火化服务',
        'desc': '引导火化'
    },
    {
        'pattern': r'可以选择土葬.*?（需符合当地法规）',
        'replacement': '建议选择火化服务（符合所有法规要求）',
        'desc': '引导火化'
    },
]

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for rule in REPLACE_PATTERNS:
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
    
    print("=" * 70)
    print("土葬选项修复报告")
    print("=" * 70)
    print(f"\n共修复 {len(fixed_files)} 个文件\n")
    
    for item in fixed_files[:30]:
        print(f"📄 {item['file']}")
        for change in item['changes']:
            print(f"   ✓ {change}")
    
    if len(fixed_files) > 30:
        print(f"\n... 还有 {len(fixed_files) - 30} 个文件未显示")

if __name__ == "__main__":
    main()
