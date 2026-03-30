#!/usr/bin/env python3
"""SEO修复脚本 - 按照用户确认的项目执行"""

from pathlib import Path
import re
import sys

docs_dir = Path('docs')
districts = [f for f in docs_dir.glob('cities/*/*/*.md') if f.name != 'index.md']

def fix_forbidden_words():
    """修复1: 清理禁用词"""
    print('='*60)
    print('【修复1: 清理禁用词】')
    print('='*60)
    
    forbidden_replacements = {
        '陵园': '纪念场所',
        '骨灰堂': '骨灰寄存处', 
        '私自建坟': '私自掩埋',
        '建坟': '安葬',
    }
    
    fixed = 0
    for d in districts:
        content = d.read_text(encoding='utf-8')
        original = content
        
        for old, new in forbidden_replacements.items():
            content = content.replace(old, new)
        
        if content != original:
            d.write_text(content, encoding='utf-8')
            fixed += 1
    
    print(f'  修复文章: {fixed}篇')
    return fixed

def fix_title():
    """修复2: 扩展Title到50-60字符"""
    print('\n' + '='*60)
    print('【修复2: 扩展Title】')
    print('='*60)
    
    fixed = 0
    for d in districts:
        content = d.read_text(encoding='utf-8')
        
        # 提取城市和区县
        parts = d.relative_to(docs_dir / 'cities').parts
        city = parts[1]
        district = parts[2].replace('宠物火化服务.md', '')
        
        # 新Title
        new_title = f'{district}宠物火化服务 - 专业宠物殡葬善终服务,告别仪式,骨灰寄存,24小时上门,单炉火化 - 百情宠物善终'
        
        # 替换
        new_content = re.sub(r'^title: .+$', f'title: {new_title}', content, flags=re.MULTILINE)
        
        if new_content != content:
            d.write_text(new_content, encoding='utf-8')
            fixed += 1
    
    print(f'  修复文章: {fixed}篇')
    return fixed

def fix_description():
    """修复3: 扩展Description到150-160字符"""
    print('\n' + '='*60)
    print('【修复3: 扩展Description】')
    print('='*60)
    
    fixed = 0
    for d in districts:
        content = d.read_text(encoding='utf-8')
        
        # 提取城市和区县
        parts = d.relative_to(docs_dir / 'cities').parts
        city = parts[1]
        district = parts[2].replace('宠物火化服务.md', '')
        
        # 新Description
        new_desc = f'{city}市{district}宠物火化服务，百情宠物善终专注宠物殡葬善终服务17年，累计服务超80000只宠物，提供告别仪式、火化、骨灰寄存、树葬纪念等全程服务，24小时上门接送，单炉火化卫生安全，专业团队全程陪同，让爱宠有尊严走完最后一程，费用透明无隐形消费，正规专业值得信赖，欢迎咨询微信923160208。'
        
        # 替换
        new_content = re.sub(r'^description: .+$', f'description: {new_desc}', content, flags=re.MULTILINE)
        
        if new_content != content:
            d.write_text(new_content, encoding='utf-8')
            fixed += 1
    
    print(f'  修复文章: {fixed}篇')
    return fixed

def fix_duplicate_components():
    """修复4: 删除重复组件"""
    print('\n' + '='*60)
    print('【修复4: 删除重复组件】')
    print('='*60)
    
    fixed = 0
    for d in districts:
        content = d.read_text(encoding='utf-8')
        original = content
        
        # 检查是否有重复的"## 相关服务"
        if content.count('## 相关服务') >= 2 and content.count('<MyContact />') >= 2:
            # 找到第一个"## 相关服务"
            first_related = content.find('## 相关服务')
            # 找到第一个<MyContact />
            first_contact = content.find('<MyContact />', first_related)
            # 找到这个<MyContact />后的换行
            end_pos = content.find('\n', first_contact + len('<MyContact />'))
            
            # 删除这一段（包括前面的空行）
            content = content[:first_related] + content[end_pos+1:]
            
            d.write_text(content, encoding='utf-8')
            fixed += 1
    
    print(f'  修复文章: {fixed}篇')
    return fixed

def verify():
    """验证修复结果"""
    print('\n' + '='*60)
    print('【验证结果】')
    print('='*60)
    
    # 检查禁用词
    forbidden_count = 0
    for d in districts[:500]:
        c = d.read_text(encoding='utf-8')
        if '陵园' in c or '骨灰堂' in c:
            forbidden_count += 1
    print(f'  禁用词残留: {forbidden_count}篇 (抽样500篇)')
    
    # 检查Title长度
    title_lens = []
    for d in districts[:100]:
        c = d.read_text(encoding='utf-8')
        tm = re.search(r'^title: (.+)$', c, re.MULTILINE)
        if tm:
            title_lens.append(len(tm.group(1)))
    avg_title = sum(title_lens)/len(title_lens) if title_lens else 0
    print(f'  Title平均长度: {avg_title:.0f}字符')
    
    # 检查Description长度
    desc_lens = []
    for d in districts[:100]:
        c = d.read_text(encoding='utf-8')
        dm = re.search(r'^description: (.+)$', c, re.MULTILINE)
        if dm:
            desc_lens.append(len(dm.group(1)))
    avg_desc = sum(desc_lens)/len(desc_lens) if desc_lens else 0
    print(f'  Description平均长度: {avg_desc:.0f}字符')
    
    # 检查重复组件
    dup_count = 0
    for d in districts[:500]:
        c = d.read_text(encoding='utf-8')
        if c.count('## 相关服务') > 1:
            dup_count += 1
    print(f'  重复组件残留: {dup_count}篇 (抽样500篇)')

if __name__ == '__main__':
    print('开始SEO修复...')
    print(f'总文章数: {len(districts)}')
    
    # 执行修复
    fix_forbidden_words()
    fix_title()
    fix_description()
    fix_duplicate_components()
    
    # 验证
    verify()
    
    print('\n' + '='*60)
    print('✅ 修复完成!')
    print('='*60)
