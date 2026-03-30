#!/usr/bin/env python3
"""修复组件顺序：Breadcrumb 应该在 MyContact 之前"""

import os
import re

def fix_component_order(filepath):
    """修复单个文件的组件顺序"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找 H1 标题后的组件顺序
        # 当前错误顺序: H1 -> MyContact -> Breadcrumb -> DistrictList
        # 正确顺序: H1 -> Breadcrumb -> MyContact -> DistrictList
        
        pattern = r'^(# .+?)\n\n<MyContact />\n\n<Breadcrumb />\n\n<DistrictList />'
        replacement = r'\1\n\n<Breadcrumb />\n\n<MyContact />\n\n<DistrictList />'
        
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if content != original_content:
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
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            
            if fix_component_order(filepath):
                fixed_count += 1
                if fixed_count % 100 == 0:
                    print(f"已修复 {fixed_count} 篇...")
    
    print(f"\n完成！共修复 {fixed_count} 篇文章的组件顺序")

if __name__ == '__main__':
    main()
