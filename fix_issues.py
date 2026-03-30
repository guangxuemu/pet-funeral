#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复重复MyContact和敏感词问题
"""
import os
import re
import glob

# 需要修复的文件
REPEAT_MYCONTACT_FILES = [
    "docs/cities/山西/忻州/河曲县宠物火化服务.md",
    "docs/cities/浙江/丽水/遂昌县宠物火化服务.md"
]

# 需要清理"坟"字的文件（不包括潞王坟乡地名）
FEN_FILES = {
    "docs/cities/江西/吉安/泰和县宠物火化服务.md": [
        ("迁坟", "迁移")
    ],
    "docs/cities/山东/临沂/莒南县宠物火化服务.md": [
        ("迁坟", "迁移")
    ],
    "docs/cities/湖南/常德/临澧县宠物火化服务.md": [
        ("挖坟", "挖掘墓地"),
        ("'坟头'", "'墓地'"),
        ("坟头", "墓地")
    ],
    "docs/cities/青海/海西/都兰县宠物火化服务.md": [
        ("坟墓", "安葬地")
    ]
}

def remove_duplicate_mycontact(filepath):
    """删除重复的MyContact组件（保留文末的，删除DistrictList后的）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # 查找 DistrictList 后、正文前的 MyContact 并删除
    # 模式：DistrictList后面跟着服务覆盖区块和MyContact
    pattern = r'(<DistrictList\s*/?>\s*\n)(\s*---\s*\n\*\*服务覆盖：\*\*.*?<MyContact\s*/?>\s*)'
    replacement = r'\1'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def clean_fen_words(filepath, replacements):
    """清理"坟"字敏感词"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        # 只替换非地名的"坟"字（排除"潞王坟乡"这种情况）
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("开始修复问题")
    print("=" * 60)
    
    # 1. 修复重复MyContact
    print("\n【修复1: 删除重复MyContact组件】")
    fixed_count = 0
    for filepath in REPEAT_MYCONTACT_FILES:
        full_path = os.path.join("/home/mz/.openclaw/workspace/pet-funeral", filepath)
        if os.path.exists(full_path):
            if remove_duplicate_mycontact(full_path):
                print(f"  ✅ 已修复: {filepath}")
                fixed_count += 1
            else:
                print(f"  ⚠️ 无需修改: {filepath}")
        else:
            print(f"  ❌ 文件不存在: {filepath}")
    print(f"  共修复: {fixed_count}篇")
    
    # 2. 清理"坟"字敏感词
    print("\n【修复2: 清理'坟'字敏感词】")
    fixed_count = 0
    for filepath, replacements in FEN_FILES.items():
        full_path = os.path.join("/home/mz/.openclaw/workspace/pet-funeral", filepath)
        if os.path.exists(full_path):
            if clean_fen_words(full_path, replacements):
                print(f"  ✅ 已修复: {filepath}")
                fixed_count += 1
            else:
                print(f"  ⚠️ 无需修改: {filepath}")
        else:
            print(f"  ❌ 文件不存在: {filepath}")
    print(f"  共修复: {fixed_count}篇")
    
    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
