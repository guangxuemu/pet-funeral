#!/usr/bin/env python3
"""修复重复的FAQ章节"""

import os
import re

def fix_duplicate_faq():
    """修复重复的FAQ"""
    
    fixed_count = 0
    errors = []
    
    for root, dirs, files in os.walk('docs/cities'):
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 检查是否有重复的FAQ标记
                # 情况1: 已有"## 四、常见问题解答"，又添加了"## 常见问题解答"
                if ('## 四、常见问题解答' in content or '## 常见问题' in content) and '## 常见问题解答\n\n**Q：' in content:
                    # 删除末尾添加的标准化FAQ（保留原有的）
                    # 找到最后一个"## 常见问题解答"的位置
                    last_faq_pos = content.rfind('## 常见问题解答')
                    
                    if last_faq_pos > 0:
                        # 保留这部分之前的内容
                        content = content[:last_faq_pos].rstrip()
                        
                        # 确保文件以<MyContact />结尾
                        if '<MyContact />' not in content[-100:]:
                            content += '\n\n<MyContact />\n'
                        
                        fixed_count += 1
                
                # 如果内容有修改，写回文件
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                
            except Exception as e:
                errors.append((filepath, str(e)))
    
    print(f"修复完成：{fixed_count}篇文章")
    if errors:
        print(f"错误数：{len(errors)}")
        for filepath, error in errors[:5]:
            print(f"  {filepath}: {error}")

if __name__ == '__main__':
    fix_duplicate_faq()
