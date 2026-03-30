#!/usr/bin/env python3
"""
宠物殡葬项目 - SEO全面优化脚本
功能：
1. 修复Title过短问题（扩展到50-60字符）
2. 修复Description过短问题（扩展到150-160字符）
3. 添加FAQ章节（缺少的文章）
4. 修复MyContact组件位置
5. 更新Keywords
"""

import os
import re
from datetime import datetime

# 统计
stats = {
    'title_fixed': 0,
    'desc_fixed': 0,
    'faq_added': 0,
    'mycontact_fixed': 0,
    'keywords_updated': 0,
    'total_checked': 0,
    'errors': []
}

def get_location_info(filepath):
    """从文件路径解析地区信息"""
    parts = filepath.split(os.sep)
    
    # 查找docs/cities的位置
    try:
        cities_idx = parts.index('cities')
        if len(parts) > cities_idx + 1:
            province = parts[cities_idx + 1] if len(parts) > cities_idx + 1 else ""
            city = parts[cities_idx + 2] if len(parts) > cities_idx + 2 else ""
            filename = parts[-1]
            district = filename.replace('宠物火化服务.md', '').replace('.md', '')
            return province, city, district
    except ValueError:
        pass
    
    return "", "", ""

def fix_frontmatter(content, province, city, district):
    """修复Frontmatter"""
    modified = False
    
    # 1. 修复Title
    title_pattern = re.compile(r'^title:\s*(.+?)$', re.MULTILINE)
    title_match = title_pattern.search(content)
    
    if title_match:
        old_title = title_match.group(1).strip()
        # 检查是否需要修复（少于40字符）
        if len(old_title) < 40:
            # 构建新Title（50-60字符）
            new_title = f"{district}宠物火化服务 - 专业宠物殡葬善终服务,告别仪式,骨灰寄存,24小时上门 - 百情宠物善终"
            content = title_pattern.sub(f'title: {new_title}', content)
            stats['title_fixed'] += 1
            modified = True
    
    # 2. 修复Description
    desc_pattern = re.compile(r'^description:\s*(.+?)$', re.MULTILINE)
    desc_match = desc_pattern.search(content)
    
    if desc_match:
        old_desc = desc_match.group(1).strip()
        # 检查是否需要修复（少于120字符）
        if len(old_desc) < 120:
            # 构建新Description（150-160字符）
            location_prefix = f"{province}{city}{district}" if province and city else district
            new_desc = f"{location_prefix}宠物火化服务，百情宠物善终专注宠物殡葬善终服务17年，累计服务超80000只宠物，提供告别仪式、火化、骨灰寄存、树葬纪念等全程服务，24小时上门接送，单炉火化卫生安全。"
            # 确保长度在150-160字符
            if len(new_desc) > 160:
                new_desc = new_desc[:157] + "..."
            content = desc_pattern.sub(f'description: {new_desc}', content)
            stats['desc_fixed'] += 1
            modified = True
    
    # 3. 更新Keywords（可选）
    keywords_pattern = re.compile(r'^keywords:\s*\[(.*?)\]$', re.MULTILINE | re.DOTALL)
    keywords_match = keywords_pattern.search(content)
    
    if keywords_match and city and district:
        # 添加长尾关键词
        new_keywords = f"[{city}宠物火化, {city}宠物殡葬, {district}宠物火化, {district}宠物殡葬, {district}宠物火化怎么收费, 宠物火化服务]"
        content = keywords_pattern.sub(f'keywords: {new_keywords}', content)
        stats['keywords_updated'] += 1
        modified = True
    
    return content, modified

def add_faq_section(content, district):
    """添加FAQ章节"""
    # 检查是否已有FAQ
    if '## 常见问题' in content or '## FAQ' in content or '## 常见问题解答' in content:
        return content, False
    
    # 构建FAQ内容
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
    
    # 在文件末尾添加（在最后一个MyContact之前或之后）
    content = content.rstrip() + faq_content
    return content, True

def fix_mycontact(content):
    """修复MyContact组件位置"""
    modified = False
    
    # 检查MyContact出现次数
    mycontact_count = content.count('<MyContact />')
    
    # 如果少于2个，需要在开头添加
    if mycontact_count < 2:
        # 在H1标题后添加MyContact
        h1_pattern = re.compile(r'^(# .+?)$', re.MULTILINE)
        h1_match = h1_pattern.search(content)
        
        if h1_match:
            insert_pos = h1_match.end()
            # 在H1后添加MyContact
            content = content[:insert_pos] + '\n\n<MyContact />' + content[insert_pos:]
            modified = True
            stats['mycontact_fixed'] += 1
    
    # 如果多于2个，删除多余的
    elif mycontact_count > 2:
        # 只保留最后两个
        parts = content.split('<MyContact />')
        if len(parts) > 3:
            # 保留前两部分和最后两部分
            content = parts[0] + '<MyContact />' + parts[1] + '<MyContact />' + '<MyContact />'.join(parts[-2:])
            modified = True
            stats['mycontact_fixed'] += 1
    
    return content, modified

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 获取地区信息
        province, city, district = get_location_info(filepath)
        
        if not district:
            return
        
        # 1. 修复Frontmatter
        content, fm_modified = fix_frontmatter(content, province, city, district)
        if fm_modified:
            modified = True
        
        # 2. 添加FAQ
        content, faq_modified = add_faq_section(content, district)
        if faq_modified:
            stats['faq_added'] += 1
            modified = True
        
        # 3. 修复MyContact
        content, mc_modified = fix_mycontact(content)
        if mc_modified:
            modified = True
        
        # 写回文件
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        stats['total_checked'] += 1
        
        # 每100篇打印进度
        if stats['total_checked'] % 100 == 0:
            print(f"已处理 {stats['total_checked']} 篇...")
        
    except Exception as e:
        stats['errors'].append((filepath, str(e)))

def main():
    """主函数"""
    print("=" * 60)
    print("开始SEO全面优化")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 遍历所有文章
    docs_dir = 'docs/cities'
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath)
    
    # 打印统计
    print()
    print("=" * 60)
    print("优化完成统计")
    print("=" * 60)
    print(f"总检查文章数: {stats['total_checked']}")
    print(f"Title修复: {stats['title_fixed']} 篇")
    print(f"Description修复: {stats['desc_fixed']} 篇")
    print(f"FAQ添加: {stats['faq_added']} 篇")
    print(f"MyContact修复: {stats['mycontact_fixed']} 篇")
    print(f"Keywords更新: {stats['keywords_updated']} 篇")
    
    if stats['errors']:
        print(f"\n错误数: {len(stats['errors'])}")
        for filepath, error in stats['errors'][:5]:
            print(f"  {filepath}: {error}")
    
    print()
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
