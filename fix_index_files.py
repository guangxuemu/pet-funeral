#!/usr/bin/env python3
"""修复所有index.md文件的Frontmatter错误"""

import os
import re

def fix_index_file(filepath, province_name):
    """修复单个index.md文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 1. 修复Title中的index错误
        if re.search(r'^title:\s*index', content, re.MULTILINE):
            content = re.sub(
                r'^title:\s*index',
                f'title: {province_name}',
                content,
                flags=re.MULTILINE
            )
            modified = True
        
        # 2. 修复Description中的index.md错误 (辽宁index.mdindex)
        if 'index.mdindex' in content:
            content = content.replace(f'{province_name}index.mdindex', f'{province_name}省')
            modified = True
        
        # 3. 修复Description中的index.md (福建index.md宠物)
        if f'{province_name}index.md' in content:
            content = content.replace(f'{province_name}index.md', f'{province_name}省')
            modified = True
        
        # 4. 修复Keywords中的index.md错误
        if 'index.md宠物' in content:
            content = content.replace('index.md宠物', f'{province_name}宠物')
            modified = True
        
        # 5. 修复Keywords中的index错误
        if 'index宠物' in content:
            content = content.replace('index宠物', f'{province_name}宠物')
            modified = True
        
        # 6. 删除多余的"**联系方式**：微信：923160208"文字（保留<MyContact />）
        if '**联系方式**：微信：923160208' in content:
            content = content.replace('**联系方式**：微信：923160208\n\n', '')
            modified = True
        
        # 写回文件
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
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
        # 只处理直接子目录下的index.md（省份页面）
        if root == docs_dir:
            continue
        
        # 确保是省份目录（只有一级子目录）
        rel_path = os.path.relpath(root, docs_dir)
        if os.sep in rel_path:
            continue
        
        if 'index.md' in files:
            filepath = os.path.join(root, 'index.md')
            # 获取省份名称
            province = os.path.basename(root)
            
            if fix_index_file(filepath, province):
                fixed_count += 1
                print(f"Fixed: {filepath}")
    
    print(f"\n完成！共修复 {fixed_count} 个index.md文件")

if __name__ == '__main__':
    main()
