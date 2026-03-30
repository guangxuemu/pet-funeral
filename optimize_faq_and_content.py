#!/usr/bin/env python3
"""
优化FAQ和内容
1. 统一55篇非标准格式FAQ为标准格式
2. 给无FAQ的区县文章添加FAQ
3. 优化Description
4. 添加内链
"""

import os
import re
import hashlib

# FAQ模板 - 多样化
FAQ_TEMPLATES = [
    """## 常见问题解答

**Q：{district}宠物火化怎么收费？**
A：宠物火化费用根据宠物体重、服务内容而定，一般几百到几千元不等。我们提供上门接送、告别仪式、骨灰寄存等一站式服务，具体费用建议添加微信923160208咨询。

**Q：{district}有正规的宠物火化机构吗？**
A：有的。百情宠物善终在{district}及周边提供专业宠物火化服务，24小时上门接送，独立火化炉，全程可陪同，正规合规。

**Q：宠物去世后怎么处理比较好？**
A：我们强烈推荐专业火化服务。相比其他方式，火化更卫生、环保、合规，且便于主人长期纪念。火化后的骨灰可以寄存、制作纪念品或生态安葬。

**Q：火化后的骨灰可以带回家吗？**
A：当然可以。火化后的骨灰经过高温处理，安全无菌，您可以带回家中纪念，也可以选择我们的骨灰寄存服务。

**Q：{district}宠物火化需要预约吗？**
A：建议提前预约，我们提供24小时服务，随时响应您的需求。添加微信923160208即可快速预约上门接运。""",

    """## 常见问题解答

**Q：{district}宠物殡葬服务怎么联系？**
A：您可以通过微信923160208联系我们，24小时在线，随时为您提供咨询和预约服务。

**Q：宠物火化费用大约多少钱？**
A：费用根据宠物体型和服务内容而定，基础火化几百元起，全套服务几千元不等。具体价格请咨询微信923160208。

**Q：{district}可以上门接宠物吗？**
A：可以的。我们提供{district}及周边24小时上门接运服务，专业团队，全程尊重，让您省心安心。

**Q：火化过程主人可以陪同吗？**
A：出于卫生和情绪考虑，火化过程不建议陪同，但我们会提供全程视频或照片记录，确保透明放心。

**Q：骨灰有哪些处理方式？**
A：骨灰可以带回家纪念、选择我们的寄存服务，或制作纪念品如骨灰钻石、纪念牌等，让爱延续。""",

    """## 常见问题解答

**Q：{district}宠物善终服务包含哪些内容？**
A：服务包含上门接运、遗体清洁、告别仪式、单独火化、骨灰处理等全流程，具体可咨询微信923160208定制方案。

**Q：宠物去世多久内处理比较好？**
A：建议尽快处理，一般在24-48小时内为佳。我们可以提供冷藏服务，确保宠物得到妥善安置。

**Q：{district}有宠物火化的地方吗？**
A：有的。百情宠物善终服务覆盖{district}及周边，提供专业火化设备和场地，正规合规。

**Q：火化费用包含哪些项目？**
A：基础费用包含接运、清洁、火化、骨灰盒；增值服务包含告别仪式、纪念品定制等，按需选择。

**Q：如何预约{district}的宠物火化服务？**
A：添加微信923160208，告知宠物情况和需求，我们会安排最近的服务时间，24小时响应。""",
]

def get_unique_faq(district, city, province):
    """生成独特的FAQ"""
    unique_key = f"{province}{city}{district}faq"
    hash_val = int(hashlib.md5(unique_key.encode()).hexdigest(), 16)
    template = FAQ_TEMPLATES[hash_val % len(FAQ_TEMPLATES)]
    return template.format(district=district, city=city, province=province)

def process_faq_files():
    """处理FAQ文件"""
    processed = 0
    added_faq = 0
    fixed_other = 0
    
    for root, dirs, files in os.walk('docs/cities'):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            filepath = os.path.join(root, file)
            
            # 跳过index.md
            if file == 'index.md':
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 获取地区信息
                parts = filepath.split(os.sep)
                district = file.replace('宠物火化服务.md', '').replace('.md', '')
                city = parts[-2] if len(parts) >= 2 else ''
                province = parts[-3] if len(parts) >= 3 else ''
                
                modified = False
                
                # 检查是否有FAQ
                has_faq = False
                faq_pattern = None
                
                # 标准格式
                if re.search(r'^## 四、常见问题', content, re.MULTILINE):
                    has_faq = True
                    faq_pattern = 'standard'
                elif re.search(r'^## 常见问题解答', content, re.MULTILINE):
                    has_faq = True
                    faq_pattern = 'standard2'
                elif re.search(r'^## 常见问题$', content, re.MULTILINE):
                    has_faq = True
                    faq_pattern = 'standard3'
                # 其他格式（需要重写的）
                elif re.search(r'Q[：:]\s*', content) or '**Q' in content:
                    has_faq = True
                    faq_pattern = 'other'
                
                # 处理其他格式的FAQ - 删除重写
                if faq_pattern == 'other':
                    # 删除旧的FAQ（从##开始到下一个##或文件结束）
                    # 找到所有可能的FAQ开始位置
                    faq_starts = [
                        (m.start(), m.group()) for m in re.finditer(r'^##+.*?(?:问题|疑问|FAQ|问答)', content, re.MULTILINE | re.IGNORECASE)
                    ]
                    
                    if faq_starts:
                        # 删除从FAQ开始到下一个主标题或文件结束
                        for start_pos, _ in faq_starts:
                            # 找到下一个主标题
                            next_heading = re.search(r'\n## [^#]', content[start_pos+1:])
                            if next_heading:
                                end_pos = start_pos + 1 + next_heading.start()
                                content = content[:start_pos] + content[end_pos:]
                            else:
                                # 删除到文件末尾（在相关服务之前）
                                related_pos = content.find('## 相关服务', start_pos)
                                if related_pos > 0:
                                    content = content[:start_pos] + content[related_pos:]
                                else:
                                    content = content[:start_pos]
                            modified = True
                            break
                    
                    # 添加新的标准FAQ
                    if modified:
                        new_faq = get_unique_faq(district, city, province)
                        # 在相关服务之前插入
                        related_pos = content.find('## 相关服务')
                        if related_pos > 0:
                            content = content[:related_pos] + new_faq + '\n\n' + content[related_pos:]
                        else:
                            content = content.rstrip() + '\n\n' + new_faq + '\n'
                        fixed_other += 1
                
                # 没有FAQ的 - 添加
                elif not has_faq:
                    new_faq = get_unique_faq(district, city, province)
                    # 在相关服务之前插入
                    related_pos = content.find('## 相关服务')
                    if related_pos > 0:
                        content = content[:related_pos] + new_faq + '\n\n' + content[related_pos:]
                    else:
                        content = content.rstrip() + '\n\n' + new_faq + '\n'
                    added_faq += 1
                    modified = True
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    processed += 1
                    if processed % 50 == 0:
                        print(f"已处理 {processed} 篇...")
                    
            except Exception as e:
                print(f"Error: {filepath} - {e}")
    
    print(f"\nFAQ处理完成！")
    print(f"  - 修复非标准格式: {fixed_other} 篇")
    print(f"  - 新增FAQ: {added_faq} 篇")
    print(f"  - 总计处理: {processed} 篇")

def optimize_description():
    """优化Description"""
    fixed = 0
    
    for root, dirs, files in os.walk('docs/cities'):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取地区信息
                parts = filepath.split(os.sep)
                district = file.replace('宠物火化服务.md', '').replace('.md', '')
                city = parts[-2] if len(parts) >= 2 else ''
                province = parts[-3] if len(parts) >= 3 else ''
                
                # 检查Description
                desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
                if desc_match:
                    old_desc = desc_match.group(1).strip()
                    
                    # 如果Description过短，优化它
                    if len(old_desc) < 120:
                        # 构建新Description
                        location = f"{province}{city}{district}" if province and city else district
                        new_desc = f"{location}宠物火化服务，百情宠物善终专注宠物殡葬善终服务17年，累计服务超80000只宠物，提供告别仪式、火化、骨灰寄存、树葬纪念等全程服务，24小时上门接送，单炉火化卫生安全，专业团队全程陪同。"
                        
                        # 确保长度合适
                        if len(new_desc) > 160:
                            new_desc = new_desc[:157] + "..."
                        
                        # 替换
                        content = re.sub(
                            r'^description:\s*.+$',
                            f'description: {new_desc}',
                            content,
                            flags=re.MULTILINE
                        )
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        fixed += 1
                        if fixed % 50 == 0:
                            print(f"已优化Description {fixed} 篇...")
                            
            except Exception as e:
                pass
    
    print(f"\nDescription优化完成！共优化 {fixed} 篇")

def add_internal_links():
    """添加内链"""
    fixed = 0
    
    for root, dirs, files in os.walk('docs/cities'):
        for file in files:
            if not file.endswith('.md') or file == 'index.md':
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                modified = False
                
                # 分离frontmatter
                frontmatter_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    body = content[len(frontmatter):]
                else:
                    frontmatter = ''
                    body = content
                
                # 添加内链（每个关键词只替换一次）
                # 火化费用 -> /faq
                if '火化费用' in body and '[火化费用]' not in body:
                    body = body.replace('火化费用', '[火化费用](/faq)', 1)
                    modified = True
                
                # 告别仪式 -> /services
                if '告别仪式' in body and '[告别仪式]' not in body and body.count('[') < 15:
                    body = body.replace('告别仪式', '[告别仪式](/services)', 1)
                    modified = True
                
                # 骨灰寄存 -> /memorial
                if '骨灰寄存' in body and '[骨灰寄存]' not in body and body.count('[') < 20:
                    body = body.replace('骨灰寄存', '[骨灰寄存](/memorial)', 1)
                    modified = True
                
                if modified:
                    content = frontmatter + body
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed += 1
                    if fixed % 200 == 0:
                        print(f"已添加内链 {fixed} 篇...")
                        
            except Exception as e:
                pass
    
    print(f"\n内链优化完成！共优化 {fixed} 篇")

if __name__ == '__main__':
    print("=" * 60)
    print("开始全面优化")
    print("=" * 60)
    
    print("\n【Phase 1】处理FAQ...")
    process_faq_files()
    
    print("\n【Phase 2】优化Description...")
    optimize_description()
    
    print("\n【Phase 3】添加内链...")
    add_internal_links()
    
    print("\n" + "=" * 60)
    print("全部优化完成！")
    print("=" * 60)
