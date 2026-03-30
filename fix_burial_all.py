#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修复：把土葬选项改为劝退土葬、引导火化
"""
import os
import re

# 修复规则：把土葬选项改为引导火化
REPLACE_RULES = [
    # 1. 服务流程中的土葬选项
    {
        'pattern': r'火化 → 骨灰寄存或土葬',
        'replacement': '火化 → 骨灰寄存或纪念安置',
        'desc': '修改服务流程'
    },
    {
        'pattern': r'骨灰寄存或土葬',
        'replacement': '骨灰寄存或纪念安置',
        'desc': '修改骨灰处理选项'
    },
    {
        'pattern': r'火化/土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    
    # 2. FAQ中关于能否土葬的回答 - 改为劝退
    {
        'pattern': r'A：可以，但.*?土葬',
        'replacement': 'A：我们强烈推荐选择专业火化服务。相比土葬，火化更卫生、环保、合规，也更便于纪念安置。',
        'desc': '劝退土葬，引导火化'
    },
    {
        'pattern': r'A：可以土葬',
        'replacement': 'A：我们强烈推荐选择专业火化服务',
        'desc': '劝退土葬'
    },
    {
        'pattern': r'A：出于.*?考虑，我们不鼓励.*?土葬',
        'replacement': 'A：出于卫生与法规考虑，我们不推荐土葬。相比之下，专业火化更安全、环保、合规，也更便于纪念安置。',
        'desc': '强化劝退土葬'
    },
    
    # 3. 骨灰处理方式
    {
        'pattern': r'可选择土葬、撒海、寄存',
        'replacement': '可选择骨灰寄存、生态纪念安置或制作纪念品',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'可选择土葬',
        'replacement': '可选择专业火化后的纪念安置',
        'desc': '删除土葬选项'
    },
    
    # 4. 其他土葬相关表述
    {
        'pattern': r'如需土葬',
        'replacement': '如需了解其他方式',
        'desc': '删除土葬引导'
    },
    {
        'pattern': r'若选择土葬',
        'replacement': '若考虑其他方式',
        'desc': '删除土葬引导'
    },
    {
        'pattern': r'若您倾向土葬',
        'replacement': '若您选择火化后的纪念安置',
        'desc': '引导火化'
    },
    
    # 5. 核心流程中的土葬
    {
        'pattern': r'专业火化/土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化或土葬',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    
    # 6. 协助土葬
    {
        'pattern': r'协助.*?土葬',
        'replacement': '协助办理火化后的纪念安置',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'办理.*?土葬',
        'replacement': '办理专业火化服务',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'提供.*?土葬',
        'replacement': '提供专业火化服务',
        'desc': '删除土葬服务'
    },
    
    # 7. 土葬作为选项的列表
    {
        'pattern': r'土葬、撒海、寄存',
        'replacement': '骨灰寄存、生态纪念安置或制作纪念品',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬、海葬或树葬',
        'replacement': '骨灰寄存、纪念品定制或生态纪念安置',
        'desc': '删除土葬/海葬选项'
    },
    
    # 8. FAQ问题修改
    {
        'pattern': r'能否选择土葬',
        'replacement': '能否选择其他纪念方式',
        'desc': '修改问题'
    },
    {
        'pattern': r'是否必须火化\?可以土葬吗\?',
        'replacement': '为什么要选择火化而不是土葬？',
        'desc': '修改问题'
    },
    {
        'pattern': r'是否必须火化\?能不能土葬\?',
        'replacement': '为什么要选择火化而不是土葬？',
        'desc': '修改问题'
    },
    {
        'pattern': r'是否必须火化\?是否可以土葬\?',
        'replacement': '为什么要选择火化而不是土葬？',
        'desc': '修改问题'
    },
    {
        'pattern': r'可以土葬吗\?',
        'replacement': '可以选择其他纪念方式吗？',
        'desc': '修改问题'
    },
    {
        'pattern': r'能土葬吗\?',
        'replacement': '有其他纪念方式吗？',
        'desc': '修改问题'
    },
    {
        'pattern': r'能不能土葬',
        'replacement': '能不能选择其他纪念方式',
        'desc': '修改问题'
    },
    {
        'pattern': r'能土葬吗',
        'replacement': '有其他纪念方式吗',
        'desc': '修改问题'
    },
    
    # 9. 更多土葬表述
    {
        'pattern': r'选择生态土葬',
        'replacement': '选择生态纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'提供指定地点协助.*?土葬',
        'replacement': '提供纪念安置指导',
        'desc': '删除土葬服务'
    },
    {
        'pattern': r'您可以根据个人意愿选择土葬',
        'replacement': '我们推荐选择专业火化服务',
        'desc': '引导火化'
    },
    {
        'pattern': r'您可以选择火化、土葬',
        'replacement': '我们推荐选择专业火化服务',
        'desc': '引导火化'
    },
    {
        'pattern': r'无论是选择火化、土葬',
        'replacement': '无论是选择单独火化或集体火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'除传统土葬外',
        'replacement': '除传统方式外',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'家庭土葬',
        'replacement': '家庭纪念安置',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'倾向土葬',
        'replacement': '倾向纪念安置',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'希望保留土葬形式',
        'replacement': '希望选择其他纪念方式',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'是否必须火化\?不能土葬吗\?',
        'replacement': '为什么要选择火化而不是土葬？',
        'desc': '修改问题'
    },
    {
        'pattern': r'能否选择不火化，直接土葬',
        'replacement': '能否选择其他纪念方式',
        'desc': '修改问题'
    },
    {
        'pattern': r'火化并非唯一选择.*?土葬',
        'replacement': '火化是最推荐的选择',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'也有部分家庭倾向土葬',
        'replacement': '也有部分家庭选择不同纪念方式',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'为什么要选择专业宠物火化而非土葬',
        'replacement': '为什么选择专业宠物火化服务',
        'desc': '删除土葬对比'
    },
    {
        'pattern': r'为什么选择宠物火化而非传统土葬',
        'replacement': '为什么选择专业宠物火化服务',
        'desc': '删除土葬对比'
    },
    {
        'pattern': r'为什么选择宠物火化而非土葬',
        'replacement': '为什么选择专业宠物火化服务',
        'desc': '删除土葬对比'
    },
    {
        'pattern': r'选择土葬、树葬、海葬或火化',
        'replacement': '选择专业火化后的多种纪念方式',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'土葬于远离水源',
        'replacement': '纪念安置需选择合适地点',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'生态安葬（土葬/树葬）',
        'replacement': '生态纪念安置（树葬纪念）',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'骨灰寄存或安葬（可选土葬/树葬）',
        'replacement': '骨灰寄存或生态纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'是否必须火化\?有没有土葬或其他选项\?',
        'replacement': '为什么要选择火化而不是其他方式？',
        'desc': '修改问题'
    },
    {
        'pattern': r'火化、土葬（需符合地方法规）',
        'replacement': '专业火化服务（符合所有法规要求）',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化、土葬或生态安葬',
        'replacement': '单独火化或集体火化',
        'desc': '删除土葬选项'
    },
    
    # 10. 更多需要修复的表述
    {
        'pattern': r'我们也了解合规的林地选址',
        'replacement': '我们也提供火化后的多种纪念安置方案',
        'desc': '删除土葬协助'
    },
    {
        'pattern': r'可以土葬吗\?',
        'replacement': '可以选择其他纪念方式吗？',
        'desc': '修改问题'
    },
    {
        'pattern': r'能否土葬',
        'replacement': '能否选择其他纪念方式',
        'desc': '修改问题'
    },
    {
        'pattern': r'是否必须火化\?可以土葬吗',
        'replacement': '为什么要选择火化而不是土葬',
        'desc': '修改问题'
    },
    
    # 11. 更多FAQ问题
    {
        'pattern': r'宠物去世了可以土葬吗',
        'replacement': '宠物去世了应该如何妥善处理',
        'desc': '修改问题'
    },
    {
        'pattern': r'小猫去世了，可以土葬吗',
        'replacement': '小猫去世了应该如何妥善处理',
        'desc': '修改问题'
    },
    {
        'pattern': r'是否必须火化\?有没有土葬或其他选项',
        'replacement': '为什么要选择火化而不是其他方式',
        'desc': '修改问题'
    },
    
    # 12. 核心流程中的土葬选项
    {
        'pattern': r'火化（可选土葬）',
        'replacement': '专业火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化（或土葬/寄存）',
        'replacement': '专业火化（可选骨灰寄存）',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'骨灰封装或土葬/海葬',
        'replacement': '骨灰封装或纪念安置',
        'desc': '删除土葬/海葬选项'
    },
    
    # 13. 提供更多选择语境中的土葬
    {
        'pattern': r'无论是传统土葬、生态林葬',
        'replacement': '无论是骨灰寄存、生态纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'无论是火化、土葬还是海葬',
        'replacement': '无论是单独火化还是集体火化',
        'desc': '删除土葬/海葬选项'
    },
    {
        'pattern': r'无论是火化、土葬还是其他形式',
        'replacement': '无论是单独火化还是集体火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'无论选择火化、土葬还是其他形式',
        'replacement': '无论选择单独火化还是集体火化',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'无论选择火化还是土葬',
        'replacement': '无论选择单独火化还是集体火化',
        'desc': '删除土葬选项'
    },
    
    # 14. 标题中的土葬对比
    {
        'pattern': r'火化还是土葬',
        'replacement': '专业宠物火化',
        'desc': '修改标题'
    },
    {
        'pattern': r'火化（可选土葬）→',
        'replacement': '专业火化 →',
        'desc': '删除土葬选项'
    },
    
    # 15. 生态安葬选项中的土葬
    {
        'pattern': r'生态林地埋葬',
        'replacement': '生态纪念安置',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'若您选择土',
        'replacement': '若您选择纪念安置',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'若坚持土葬',
        'replacement': '若考虑其他方式',
        'desc': '删除土葬表述'
    },
    {
        'pattern': r'土葬（注意：城市区域多不支持野外土葬）',
        'replacement': '其他方式（注意：城市区域多不支持土葬）',
        'desc': '修改表述'
    },
    
    # 16. 更多核心流程中的土葬
    {
        'pattern': r'火化（可选土葬）→ 骨灰返还或安葬',
        'replacement': '专业火化 → 骨灰返还或纪念安置',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'火化（可选土葬）→',
        'replacement': '专业火化 →',
        'desc': '删除土葬选项'
    },
    {
        'pattern': r'若您更倾向传统方式，也可选择生态林地埋葬',
        'replacement': '我们也提供多种生态纪念安置方案',
        'desc': '删除土葬选项'
    },
]

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for rule in REPLACE_RULES:
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
    print("土葬选项全面修复报告")
    print("=" * 70)
    print(f"\n共修复 {len(fixed_files)} 个文件\n")
    
    for item in fixed_files[:50]:
        print(f"📄 {item['file']}")
        for change in item['changes'][:3]:  # 只显示前3个修改
            print(f"   ✓ {change}")
    
    if len(fixed_files) > 50:
        print(f"\n... 还有 {len(fixed_files) - 50} 个文件未显示")

if __name__ == "__main__":
    main()
