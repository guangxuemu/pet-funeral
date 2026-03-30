#!/usr/bin/env python3
"""
批量修改宠物殡葬内容：
1. 删除海葬相关内容
2. 模糊告别仪式描述
3. 骨灰处理改为自行处理（删除寄存服务）
"""

import os
import re
import glob
from pathlib import Path

def fix_sea_burial_content(content):
    """删除海葬相关内容"""
    # 删除海边告别仪式
    content = re.sub(r'海边告别仪式[、,，]?', '', content)
    content = re.sub(r'海边告别[、,，]?', '', content)
    # 删除海葬服务
    content = re.sub(r'骨灰海葬[、,，]?', '', content)
    content = re.sub(r'海葬服务[、,，]?', '', content)
    content = re.sub(r'海葬[、,，]?', '', content)
    # 清理多余的顿号、逗号
    content = re.sub(r'[、,，]{2,}', '、', content)
    content = re.sub(r'[、,，] +[、,，]', '、', content)
    content = re.sub(r'、+', '、', content)
    content = re.sub(r'，+', '，', content)
    content = re.sub(r',+', ',', content)
    # 清理 description 中的多余标点
    content = re.sub(r'、 +', '、', content)
    content = re.sub(r'， +', '，', content)
    return content

def fix_farewell_ritual(content):
    """模糊告别仪式描述"""
    # 保留链接，但简化描述
    # 将具体描述改为中性描述
    patterns = [
        (r'温馨告别室，可留存毛发、爪印、足印', '可根据需要留存纪念'),
        (r'静默告别仪式', '告别仪式'),
        (r'温馨告别仪式', '告别仪式'),
        (r'提供告别仪式引导与纪念建议', '提供纪念建议'),
        (r'设有小型告别厅', ''),
        (r'您可以携带照片、玩具等.*，为爱宠举办一场温馨的私人告别仪式，表达您深深的怀念', ''),
        (r'举办.*告别仪式', ''),
        (r'有助于提升告别仪式的情感温度', ''),
        (r'虽然无法举行\[告别仪式\]\(/services\)，但我们仍会以最尊重的态度处理', ''),
    ]
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    return content

def fix_ash_handling(content):
    """修改骨灰处理方式 - 强调自行处理"""
    # 删除骨灰寄存服务
    content = re.sub(r'、?骨灰寄存[^，,。]*', '', content)
    content = re.sub(r'骨灰寄存[^，,。]*[、,，]?', '', content)
    content = re.sub(r'、?骨灰寄存服务[^，,。]*', '', content)
    content = re.sub(r'寄存服务[^，,。]*[、,，]?', '', content)
    # 删除撒散服务
    content = re.sub(r'、?撒散服务[^，,。]*', '', content)
    content = re.sub(r'撒散服务[^，,。]*[、,，]?', '', content)
    # 修改骨灰处理描述
    content = re.sub(
        r'可选择：\s*1\. \*\*带回安葬\*\*：[^\n]*\s*2\. \*\*骨灰寄存\*\*：[^\n]*\s*3\. \*\*撒散服务\*\*：[^\n]*\s*4\. \*\*制作纪念品\*\*：[^\n]*',
        '火化完成后，骨灰由宠物主人自行带走处理。您可以选择带回家中纪念，或根据当地规定妥善安置。',
        content
    )
    # 修改FAQ中的骨灰处理
    content = re.sub(
        r'可选择：\s*\n1\. \*\*带回安葬\*\*[^\n]*\n2\. \*\*骨灰寄存\*\*[^\n]*\n3\. \*\*撒散服务\*\*[^\n]*\n4\. \*\*制作纪念品\*\*[^\n]*',
        '火化完成后，骨灰由宠物主人自行带走处理。您可以选择带回家中纪念，或根据当地规定妥善安置。',
        content
    )
    # 修改"也可以选择我们的骨灰寄存服务"
    content = re.sub(
        r'也可以选择我们的骨灰寄存服务',
        '请根据您的意愿自行处理',
        content
    )
    content = re.sub(
        r'您可以选择带回家中纪念，也可以选择我们的骨灰寄存服务',
        '骨灰由您自行带走处理',
        content
    )
    # 删除骨灰寄存相关FAQ
    content = re.sub(
        r'### Q: .*寄存.*\?\s*\n[^#]*',
        '',
        content
    )
    # 清理多余标点
    content = re.sub(r'[、,，]{2,}', '、', content)
    content = re.sub(r'、 +', '、', content)
    return content

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 应用所有修复
        content = fix_sea_burial_content(content)
        content = fix_farewell_ritual(content)
        content = fix_ash_handling(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    docs_dir = Path('/home/mz/.openclaw/workspace/pet-funeral/docs')
    md_files = list(docs_dir.rglob('*.md'))
    
    modified = 0
    sea_burial_files = 0
    
    for filepath in md_files:
        # 检查是否包含海葬相关内容
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if re.search(r'骨灰海葬|海边告别|海葬服务', content):
                sea_burial_files += 1
        except:
            pass
        
        if process_file(filepath):
            modified += 1
    
    print(f"Total files: {len(md_files)}")
    print(f"Files with sea burial content: {sea_burial_files}")
    print(f"Modified files: {modified}")

if __name__ == '__main__':
    main()
