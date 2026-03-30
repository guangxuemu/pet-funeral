#!/usr/bin/env python3
"""添加内链优化 - 在文章中添加锚文本链接"""

import os
import re
import random

# 内链关键词映射
INTERNAL_LINKS = {
    '宠物火化': '/cities/',
    '宠物殡葬': '/services',
    '告别仪式': '/services',
    '骨灰寄存': '/memorial',
    '宠物纪念品': '/memorial',
    '火化费用': '/faq',
    '怎么收费': '/faq',
    '上门接送': '/services',
    '微信咨询': '',  # 不链接，保持微信组件
    '24小时': '',
}

def add_internal_links_to_file(filepath, province, city, district):
    """为单个文件添加内链"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 只在正文中添加链接（不在frontmatter和代码块中）
        # 分离frontmatter
        frontmatter_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            body = content[len(frontmatter):]
        else:
            frontmatter = ''
            body = content
        
        # 在正文中添加内链（每个关键词只替换一次，避免过度优化）
        # 1. 添加火化费用内链
        if '火化费用' in body and '[火化费用]' not in body:
            body = body.replace(
                '火化费用',
                '[火化费用](/faq)',
                1
            )
            modified = True
        
        # 2. 添加告别仪式内链（如果还没有）
        if '告别仪式' in body and '[告别仪式]' not in body and body.count('[') < 10:
            body = body.replace(
                '告别仪式',
                '[告别仪式](/services)',
                1
            )
            modified = True
        
        # 3. 添加骨灰寄存内链
        if '骨灰寄存' in body and '[骨灰寄存]' not in body and body.count('[') < 15:
            body = body.replace(
                '骨灰寄存',
                '[骨灰寄存](/memorial)',
                1
            )
            modified = True
        
        # 4. 添加宠物纪念品内链
        if '纪念品' in body and '[纪念品]' not in body and body.count('[') < 20:
            body = body.replace(
                '纪念品',
                '[纪念品](/memorial)',
                1
            )
            modified = True
        
        # 重新组合
        new_content = frontmatter + body
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error: {filepath} - {e}")
        return False

def main():
    """主函数"""
    fixed_count = 0
    
    docs_dir = 'docs/cities'
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith('.md') or file == 'index.md':
                continue
                
            filepath = os.path.join(root, file)
            
            # 获取地区信息
            parts = filepath.split(os.sep)
            district = file.replace('宠物火化服务.md', '').replace('.md', '')
            city = parts[-2] if len(parts) >= 2 else ''
            province = parts[-3] if len(parts) >= 3 else ''
            
            if add_internal_links_to_file(filepath, province, city, district):
                fixed_count += 1
                if fixed_count % 200 == 0:
                    print(f"已优化 {fixed_count} 篇...")
    
    print(f"\n完成！共为 {fixed_count} 篇文章添加内链")

if __name__ == '__main__':
    main()
