#!/usr/bin/env python3
"""
执行全部SEO优化
批次1: Title添加疑问词
批次2: FAQ扩展
批次3: Keywords扩展
批次4: 正文开头优化
"""

import os
import re
import hashlib

print("=" * 70)
print("开始执行全部SEO优化")
print("=" * 70)

# ========== 批次1: Title添加疑问词 ==========
print("\n【批次1/4】Title添加疑问词...")

def optimize_title(filepath, district, city, province):
    """优化Title，添加疑问词"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取当前Title
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if not title_match:
            return False
        
        old_title = title_match.group(1).strip()
        
        # 如果Title已经包含疑问词，跳过
        if '?' in old_title or '怎么' in old_title or '怎么办' in old_title:
            return False
        
        # 构建新Title（添加疑问词）
        # 模板: {district}宠物火化|宠物去世后怎么处理|怎么收费 - 百情宠物善终
        new_title = f"{district}宠物火化服务|宠物去世后怎么处理|怎么收费 - 百情宠物善终"
        
        # 确保长度在50-60字符
        if len(new_title) > 60:
            new_title = new_title[:57] + "..."
        
        # 替换
        content = re.sub(
            r'^title:\s*.+$',
            f'title: {new_title}',
            content,
            flags=re.MULTILINE
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except:
        return False

title_count = 0
for root, dirs, files in os.walk('docs/cities'):
    for file in files:
        if not file.endswith('.md') or file == 'index.md':
            continue
        
        filepath = os.path.join(root, file)
        parts = filepath.split(os.sep)
        district = file.replace('宠物火化服务.md', '').replace('.md', '')
        city = parts[-2] if len(parts) >= 2 else ''
        province = parts[-3] if len(parts) >= 3 else ''
        
        if optimize_title(filepath, district, city, province):
            title_count += 1
            if title_count % 500 == 0:
                print(f"  已优化 {title_count} 篇Title...")

print(f"  Title优化完成: {title_count} 篇")

# ========== 批次2: FAQ扩展 ==========
print("\n【批次2/4】FAQ扩展（新增5个Q&A）...")

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
]

def get_faq(district, city, province):
    """获取FAQ模板"""
    unique_key = f"{province}{city}{district}"
    hash_val = int(hashlib.md5(unique_key.encode()).hexdigest(), 16)
    template = FAQ_TEMPLATES[hash_val % len(FAQ_TEMPLATES)]
    return template.format(district=district, city=city, province=province)

def extend_faq(filepath, district, city, province):
    """扩展FAQ"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有标准FAQ
        has_standard = False
        if re.search(r'^## 四、常见问题', content, re.MULTILINE):
            has_standard = True
        elif re.search(r'^## 常见问题解答', content, re.MULTILINE):
            has_standard = True
        
        if not has_standard:
            # 添加新FAQ
            new_faq = get_faq(district, city, province)
            related_pos = content.find('## 相关服务')
            if related_pos > 0:
                content = content[:related_pos] + new_faq + '\n\n' + content[related_pos:]
            else:
                content = content.rstrip() + '\n\n' + new_faq + '\n'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except:
        return False

faq_count = 0
for root, dirs, files in os.walk('docs/cities'):
    for file in files:
        if not file.endswith('.md') or file == 'index.md':
            continue
        
        filepath = os.path.join(root, file)
        parts = filepath.split(os.sep)
        district = file.replace('宠物火化服务.md', '').replace('.md', '')
        city = parts[-2] if len(parts) >= 2 else ''
        province = parts[-3] if len(parts) >= 3 else ''
        
        if extend_faq(filepath, district, city, province):
            faq_count += 1
            if faq_count % 200 == 0:
                print(f"  已添加FAQ {faq_count} 篇...")

print(f"  FAQ扩展完成: {faq_count} 篇")

# ========== 批次3: Keywords扩展 ==========
print("\n【批次3/4】Keywords扩展...")

def extend_keywords(filepath, district, city, province):
    """扩展Keywords"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取当前Keywords
        kw_match = re.search(r'^keywords:\s*\[(.*?)\]', content, re.MULTILINE | re.DOTALL)
        if not kw_match:
            return False
        
        old_kw = kw_match.group(1).strip()
        
        # 如果已经有很多关键词，跳过
        if old_kw.count(',') >= 9:
            return False
        
        # 构建新Keywords（添加长尾词）
        new_keywords = f"[{city}宠物火化, {city}宠物殡葬, {district}宠物火化, {district}宠物殡葬, {district}宠物火化怎么收费, 宠物去世后怎么处理, {district}宠物善终服务, 宠物火化上门服务]"
        
        content = re.sub(
            r'^keywords:\s*\[.*?\]',
            f'keywords: {new_keywords}',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except:
        return False

kw_count = 0
for root, dirs, files in os.walk('docs/cities'):
    for file in files:
        if not file.endswith('.md') or file == 'index.md':
            continue
        
        filepath = os.path.join(root, file)
        parts = filepath.split(os.sep)
        district = file.replace('宠物火化服务.md', '').replace('.md', '')
        city = parts[-2] if len(parts) >= 2 else ''
        province = parts[-3] if len(parts) >= 3 else ''
        
        if extend_keywords(filepath, district, city, province):
            kw_count += 1
            if kw_count % 500 == 0:
                print(f"  已优化Keywords {kw_count} 篇...")

print(f"  Keywords扩展完成: {kw_count} 篇")

# ========== 批次4: 正文开头优化 ==========
print("\n【批次4/4】正文开头优化...")

def optimize_intro(filepath, district, city, province):
    """优化开头段落"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到DistrictList后的开头段落
        pattern = r'(<DistrictList />\n\n\n+)(.*?)(\n\n---|\n##)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return False
        
        old_intro = match.group(2).strip()
        
        # 如果已经包含疑问词，跳过
        if '怎么处理' in old_intro or '怎么办' in old_intro:
            return False
        
        # 构建新开头（融入疑问词）
        new_intro = f"当**宠物去世后怎么处理**成为许多{city}家长的困扰，我们理解这份不舍与迷茫。**狗狗死了怎么办**？在百情宠物善终，我们提供{district}专业的火化服务，24小时上门接运，让爱宠有尊严地告别。"
        
        content = content.replace(old_intro, new_intro, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except:
        return False

intro_count = 0
for root, dirs, files in os.walk('docs/cities'):
    for file in files:
        if not file.endswith('.md') or file == 'index.md':
            continue
        
        filepath = os.path.join(root, file)
        parts = filepath.split(os.sep)
        district = file.replace('宠物火化服务.md', '').replace('.md', '')
        city = parts[-2] if len(parts) >= 2 else ''
        province = parts[-3] if len(parts) >= 3 else ''
        
        if optimize_intro(filepath, district, city, province):
            intro_count += 1
            if intro_count % 500 == 0:
                print(f"  已优化开头 {intro_count} 篇...")

print(f"  开头优化完成: {intro_count} 篇")

print("\n" + "=" * 70)
print("全部优化完成！")
print("=" * 70)
print(f"\n优化统计:")
print(f"  - Title优化: {title_count} 篇")
print(f"  - FAQ扩展: {faq_count} 篇")
print(f"  - Keywords扩展: {kw_count} 篇")
print(f"  - 开头优化: {intro_count} 篇")
print(f"  - 总计: {title_count + faq_count + kw_count + intro_count} 篇")
