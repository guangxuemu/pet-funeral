#!/usr/bin/env python3
"""检查缺少FAQ的文章"""

import os

missing_faq_files = []

for root, dirs, files in os.walk('docs/cities'):
    for file in files:
        if not file.endswith('.md') or file == 'index.md':
            continue
        
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有任何FAQ标记
            has_faq = ('## 四、常见问题' in content or 
                      '## 常见问题解答' in content or 
                      '## FAQ' in content)
            
            if not has_faq:
                missing_faq_files.append(filepath)
                
        except:
            pass

print(f"缺少FAQ的文章: {len(missing_faq_files)}篇")
print("\n前10篇示例:")
for fp in missing_faq_files[:10]:
    print(f"  {fp}")

# 检查这些文章末尾是否有标准化的FAQ内容
print("\n\n检查是否有标准化FAQ内容...")
for fp in missing_faq_files[:3]:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n=== {fp} 末尾50字符 ===")
    print(content[-150:])
