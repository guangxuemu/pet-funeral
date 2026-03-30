#!/usr/bin/env python3
"""为缺少FAQ的文章添加标准化FAQ"""

import os
import re

def get_location_info(filepath):
    """从文件路径解析地区信息"""
    parts = filepath.split(os.sep)
    try:
        cities_idx = parts.index('cities')
        if len(parts) > cities_idx + 1:
            district = parts[-1].replace('宠物火化服务.md', '').replace('.md', '')
            return district
    except ValueError:
        pass
    return ""

def add_faq_to_file(filepath):
    """为单个文件添加FAQ"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 再次确认没有FAQ
        if ('## 四、常见问题' in content or 
            '## 常见问题解答' in content or 
            '## FAQ' in content):
            return False
        
        district = get_location_info(filepath)
        if not district:
            return False
        
        # 构建标准化FAQ
        faq_content = f"""

## 常见问题解答

**Q：{district}宠物火化怎么收费？**
A：宠物火化费用主要和宠物体重、服务内容相关，一般几百到几千元不等。我们提供上门接送、告别仪式、骨灰寄存等一站式服务，具体费用建议添加微信923160208咨询。

**Q：{district}有没有宠物火化殡葬处？**
A：有的。百情宠物善终在{district}及周边提供专业宠物火化服务，24小时上门接送，独立火化炉，全程可陪同。

**Q：宠物死了怎么处理比较好？**
A：我们强烈推荐选择专业火化服务。相比土葬，火化更卫生、环保、合规，且便于主人长期纪念。火化后的骨灰可以寄存、制作纪念品或生态安葬。

**Q：火化后骨灰可以带回家吗？**
A：当然可以。火化后的骨灰经过高温处理，安全无菌，您可以带回家中纪念，也可以选择我们的骨灰寄存服务。

**Q：{district}宠物火化需要预约吗？**
A：建议提前预约，我们提供24小时服务，随时响应您的需求。添加微信923160208即可快速预约。
"""
        
        # 在文件末尾添加（在相关服务之前）
        # 找到"## 相关服务"的位置
        related_pos = content.find('## 相关服务')
        if related_pos > 0:
            # 在相关服务之前插入FAQ
            content = content[:related_pos] + faq_content + '\n' + content[related_pos:]
        else:
            # 如果没有相关服务，在文件末尾添加
            content = content.rstrip() + faq_content + '\n'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error: {filepath} - {e}")
        return False

def main():
    """主函数"""
    added_count = 0
    
    for root, dirs, files in os.walk('docs/cities'):
        for file in files:
            if not file.endswith('.md') or file == 'index.md':
                continue
            
            filepath = os.path.join(root, file)
            
            # 检查是否缺少FAQ
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_faq = ('## 四、常见问题' in content or 
                          '## 常见问题解答' in content or 
                          '## FAQ' in content)
                
                if not has_faq:
                    if add_faq_to_file(filepath):
                        added_count += 1
                        if added_count % 50 == 0:
                            print(f"已添加 {added_count} 篇...")
                            
            except:
                pass
    
    print(f"\n完成！共为 {added_count} 篇文章添加了FAQ")

if __name__ == '__main__':
    main()
