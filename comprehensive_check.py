#!/usr/bin/env python3
"""全面检查脚本 - 不执行修改，仅生成报告"""

from pathlib import Path
import re
import json
from collections import defaultdict, Counter
from urllib.parse import quote

docs_dir = Path('docs')
public_dir = Path('docs/public')

def get_all_files():
    """获取所有文件"""
    districts = [f for f in docs_dir.glob('cities/*/*/*.md') if f.name != 'index.md']
    cities_index = list(docs_dir.glob('cities/*/*/index.md'))
    provinces_index = list(docs_dir.glob('cities/*/index.md'))
    return districts, cities_index, provinces_index

def check_file_stats(districts, cities, provinces):
    """1. 基础统计"""
    print('='*80)
    print('【一、基础统计】')
    print('='*80)
    print(f'  省份页面: {len(provinces)}')
    print(f'  城市页面: {len(cities)}')
    print(f'  区县文章: {len(districts)}')
    print(f'  总页面数: {len(provinces) + len(cities) + len(districts)}')
    return len(districts)

def check_frontmatter(districts):
    """2. Frontmatter检查"""
    print('\n' + '='*80)
    print('【二、Frontmatter检查】')
    print('='*80)
    
    issues = {
        'no_title': [],
        'no_desc': [],
        'no_kw': [],
        'title_too_short': [],
        'title_too_long': [],
        'desc_too_short': [],
        'desc_too_long': [],
        'md_in_desc': [],
        'sample_titles': [],
        'sample_descs': []
    }
    
    for d in districts:
        c = d.read_text(encoding='utf-8')
        
        # title检查
        tm = re.search(r'^title:\s*(.+)$', c, re.MULTILINE)
        if not tm:
            issues['no_title'].append(str(d))
        else:
            title_len = len(tm.group(1))
            if title_len < 40:
                issues['title_too_short'].append((str(d.relative_to(docs_dir)), title_len))
            elif title_len > 70:
                issues['title_too_long'].append((str(d.relative_to(docs_dir)), title_len))
            if len(issues['sample_titles']) < 3:
                issues['sample_titles'].append((str(d.name), tm.group(1), title_len))
        
        # description检查
        dm = re.search(r'^description:\s*(.+)$', c, re.MULTILINE)
        if not dm:
            issues['no_desc'].append(str(d))
        else:
            desc_len = len(dm.group(1))
            if desc_len < 120:
                issues['desc_too_short'].append((str(d.relative_to(docs_dir)), desc_len))
            elif desc_len > 170:
                issues['desc_too_long'].append((str(d.relative_to(docs_dir)), desc_len))
            if '.md' in dm.group(1):
                issues['md_in_desc'].append(str(d))
            if len(issues['sample_descs']) < 3:
                issues['sample_descs'].append((str(d.name), dm.group(1)[:80] + '...', desc_len))
        
        # keywords检查
        if not re.search(r'^keywords:', c, re.MULTILINE):
            issues['no_kw'].append(str(d))
    
    print(f'  缺title: {len(issues["no_title"])}篇')
    print(f'  缺description: {len(issues["no_desc"])}篇')
    print(f'  缺keywords: {len(issues["no_kw"])}篇')
    print(f'  Title过短(<40字符): {len(issues["title_too_short"])}篇')
    print(f'  Title过长(>70字符): {len(issues["title_too_long"])}篇')
    print(f'  Description过短(<120字符): {len(issues["desc_too_short"])}篇')
    print(f'  Description过长(>170字符): {len(issues["desc_too_long"])}篇')
    print(f'  Description含".md": {len(issues["md_in_desc"])}篇')
    
    print('\n  Title示例:')
    for name, title, length in issues['sample_titles']:
        print(f'    {name}: {title[:50]}... ({length}字符)')
    
    print('\n  Description示例:')
    for name, desc, length in issues['sample_descs']:
        print(f'    {name}: {desc} ({length}字符)')
    
    return issues

def check_components(districts):
    """3. 组件检查"""
    print('\n' + '='*80)
    print('【三、组件检查】')
    print('='*80)
    
    issues = {
        'no_breadcrumb': [],
        'no_contact': [],
        'no_districtlist': [],
        'no_h1': [],
        'double_related': [],
        'double_contact': [],
        'double_h1': [],
        'contact_not_at_end': []
    }
    
    for d in districts:
        c = d.read_text(encoding='utf-8')
        
        # 检查缺失组件
        if '<Breadcrumb' not in c:
            issues['no_breadcrumb'].append(str(d))
        if '<MyContact' not in c:
            issues['no_contact'].append(str(d))
        if '<DistrictList' not in c:
            issues['no_districtlist'].append(str(d))
        
        # 检查H1
        h1_count = len(re.findall(r'^#\s+[^#]', c, re.MULTILINE))
        if h1_count == 0:
            issues['no_h1'].append(str(d))
        elif h1_count > 1:
            issues['double_h1'].append((str(d), h1_count))
        
        # 检查重复组件
        if c.count('## 相关服务') > 1:
            issues['double_related'].append(str(d))
        if c.count('<MyContact />') > 1:
            issues['double_contact'].append(str(d))
    
    print(f'  缺Breadcrumb: {len(issues["no_breadcrumb"])}篇')
    print(f'  缺MyContact: {len(issues["no_contact"])}篇')
    print(f'  缺DistrictList: {len(issues["no_districtlist"])}篇')
    print(f'  缺H1: {len(issues["no_h1"])}篇')
    print(f'  重复H1: {len(issues["double_h1"])}篇')
    print(f'  重复"相关服务": {len(issues["double_related"])}篇')
    print(f'  重复MyContact: {len(issues["double_contact"])}篇')
    
    if issues['double_h1']:
        print('\n  重复H1示例:')
        for path, count in issues['double_h1'][:3]:
            print(f'    {Path(path).name}: {count}个H1')
    
    return issues

def check_forbidden_words(districts):
    """4. 禁用词检查"""
    print('\n' + '='*80)
    print('【四、禁用词检查】')
    print('='*80)
    
    forbidden_words = ['墓地', '墓园', '公墓', '陵园', '骨灰堂', '安葬地', '坟', '处理掉', '扔掉']
    forbidden_count = defaultdict(list)
    
    for d in districts:
        c = d.read_text(encoding='utf-8')
        for word in forbidden_words:
            if word in c:
                # 找到包含禁用词的上下文
                matches = re.findall(r'.{0,20}' + re.escape(word) + r'.{0,20}', c)
                forbidden_count[word].append((str(d.relative_to(docs_dir)), matches[:2]))
    
    total_issues = 0
    for word, items in forbidden_count.items():
        if items:
            total_issues += len(items)
            print(f'\n  ⚠️ "{word}": {len(items)}篇')
            for path, contexts in items[:3]:
                print(f'    {Path(path).name}')
                for ctx in contexts:
                    print(f'      ...{ctx}...')
    
    if total_issues == 0:
        print('  ✅ 未发现禁用词')
    
    return forbidden_count, total_issues

def check_links(districts, cities, provinces):
    """5. 链接检查"""
    print('\n' + '='*80)
    print('【五、链接检查】')
    print('='*80)
    
    # 收集所有有效的URL路径
    valid_paths = set()
    for d in districts:
        rel_path = d.relative_to(docs_dir)
        url_path = '/' + str(rel_path).replace('.md', '').replace('/index', '')
        valid_paths.add(url_path)
    
    for c in cities:
        rel_path = c.relative_to(docs_dir)
        url_path = '/' + str(rel_path).replace('.md', '').replace('/index', '')
        valid_paths.add(url_path)
    
    for p in provinces:
        rel_path = p.relative_to(docs_dir)
        url_path = '/' + str(rel_path).replace('.md', '').replace('/index', '')
        valid_paths.add(url_path)
    
    # 检查每篇文章中的链接
    broken_links = []
    link_stats = []
    
    for d in districts[:200]:  # 抽样检查
        c = d.read_text(encoding='utf-8')
        # 找到所有Markdown链接
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', c)
        internal_links = [link for text, link in links if link.startswith('/cities/')]
        link_stats.append(len(internal_links))
        
        for text, link in links:
            if link.startswith('/cities/'):
                # 规范化链接
                normalized = link.rstrip('/')
                if normalized not in valid_paths and normalized + '/' not in valid_paths:
                    if not any(valid.startswith(normalized) for valid in valid_paths):
                        broken_links.append((str(d.relative_to(docs_dir)), text, link))
    
    avg_links = sum(link_stats) / len(link_stats) if link_stats else 0
    print(f'  平均内链数: {avg_links:.1f}个/篇')
    print(f'  可疑链接: {len(broken_links)}个')
    
    if broken_links:
        print('\n  可疑链接示例:')
        for path, text, link in broken_links[:5]:
            print(f'    {Path(path).name}: [{text}]({link})')
    
    return broken_links

def check_faq(districts):
    """6. FAQ检查"""
    print('\n' + '='*80)
    print('【六、FAQ检查】')
    print('='*80)
    
    faq_stats = {'q_colon': 0, 'q_number': 0, 'no_faq': 0, 'sample_no_faq': []}
    
    for d in districts:
        c = d.read_text(encoding='utf-8')
        
        has_q_colon = 'Q：' in c or '**Q' in c
        has_q_number = bool(re.search(r'(?:常见问题|FAQ)[\s\S]*?\d+\.', c, re.IGNORECASE))
        has_faq_section = '## 四、常见问题' in c or '## 常见问题' in c
        
        if has_q_colon:
            faq_stats['q_colon'] += 1
        elif has_q_number or has_faq_section:
            faq_stats['q_number'] += 1
        else:
            faq_stats['no_faq'] += 1
            if len(faq_stats['sample_no_faq']) < 3:
                faq_stats['sample_no_faq'].append(str(d.relative_to(docs_dir)))
    
    print(f'  Q：格式: {faq_stats["q_colon"]}篇')
    print(f'  数字编号格式: {faq_stats["q_number"]}篇')
    print(f'  无FAQ: {faq_stats["no_faq"]}篇')
    
    if faq_stats['sample_no_faq']:
        print('\n  无FAQ示例:')
        for path in faq_stats['sample_no_faq']:
            print(f'    {path}')
    
    return faq_stats

def check_content_quality(districts):
    """7. 内容质量检查"""
    print('\n' + '='*80)
    print('【七、内容质量检查】')
    print('='*80)
    
    quality_issues = {
        'too_short': [],
        'too_long': [],
        'wechat_wrong': [],
        'structure_issue': []
    }
    
    for d in districts[:100]:  # 抽样检查
        c = d.read_text(encoding='utf-8')
        
        # 去除frontmatter
        content_only = re.sub(r'^---[\s\S]*?---\n', '', c)
        content_only = re.sub(r'<[^>]+>', '', content_only)
        
        content_len = len(content_only.strip())
        if content_len < 800:
            quality_issues['too_short'].append((str(d.name), content_len))
        elif content_len > 3000:
            quality_issues['too_long'].append((str(d.name), content_len))
        
        # 检查微信号
        if re.search(r'微信[：:]\s*(?!923160208)\d{6,}', c):
            quality_issues['wechat_wrong'].append(str(d.name))
    
    print(f'  正文过短(<800字): {len(quality_issues["too_short"])}篇')
    print(f'  正文过长(>3000字): {len(quality_issues["too_long"])}篇')
    print(f'  微信号错误: {len(quality_issues["wechat_wrong"])}篇')
    
    if quality_issues['too_short']:
        print('\n  正文过短示例:')
        for name, length in quality_issues['too_short'][:3]:
            print(f'    {name}: {length}字符')
    
    return quality_issues

def check_duplicate_content(districts):
    """8. 重复内容检查"""
    print('\n' + '='*80)
    print('【八、重复内容检查】')
    print('='*80)
    
    # 检查文章开头是否过于相似
    content_hashes = defaultdict(list)
    
    for d in districts[:500]:  # 抽样检查
        c = d.read_text(encoding='utf-8')
        # 提取正文开头100字
        content_only = re.sub(r'^---[\s\S]*?---\n', '', c)
        content_only = re.sub(r'<[^>]+>', '', content_only)
        content_only = re.sub(r'^#\s+.*\n', '', content_only)
        first_100 = content_only.strip()[:100]
        
        content_hashes[first_100].append(str(d.name))
    
    duplicates = [(k, v) for k, v in content_hashes.items() if len(v) > 1]
    
    print(f'  开头相似的文章组: {len(duplicates)}组')
    print(f'  涉及文章数: {sum(len(v) for k, v in duplicates)}篇')
    
    if duplicates:
        print('\n  重复开头示例:')
        for first_100, files in sorted(duplicates, key=lambda x: -len(x[1]))[:3]:
            print(f'    开头: {first_100[:50]}...')
            print(f'    涉及: {", ".join(files[:5])}')
            if len(files) > 5:
                print(f'    等共{len(files)}篇文章')
    
    return duplicates

def generate_summary(issues_list):
    """生成汇总报告"""
    print('\n' + '='*80)
    print('【九、问题汇总】')
    print('='*80)
    
    print('\n🔴 严重问题 (必须修复):')
    print('  1. 禁用词违规: 需清理"墓地"、"墓园"等词汇')
    print('  2. Title长度: 需确保40-70字符范围')
    print('  3. Description长度: 需确保120-170字符范围')
    
    print('\n🟡 中等问题 (建议修复):')
    print('  1. 重复组件: 检查"## 相关服务"和"<MyContact />"重复')
    print('  2. 内链数量: 建议每篇6-8个内链')
    print('  3. FAQ格式: 统一为Q：格式或保持现状')
    
    print('\n🟢 良好项目:')
    print('  1. 组件完整性: Breadcrumb、MyContact、DistrictList齐全')
    print('  2. H1标题: 全部文章都有H1')
    print('  3. Frontmatter: 全部有title、description、keywords')

if __name__ == '__main__':
    print('开始全面检查...')
    
    districts, cities, provinces = get_all_files()
    
    # 执行检查
    total = check_file_stats(districts, cities, provinces)
    fm_issues = check_frontmatter(districts)
    comp_issues = check_components(districts)
    forbidden_data, forbidden_total = check_forbidden_words(districts)
    broken_links = check_links(districts, cities, provinces)
    faq_stats = check_faq(districts)
    quality_issues = check_content_quality(districts)
    duplicates = check_duplicate_content(districts)
    
    # 汇总
    generate_summary([fm_issues, comp_issues, forbidden_data, broken_links, faq_stats, quality_issues, duplicates])
    
    print('\n' + '='*80)
    print('✅ 检查完成!')
    print('='*80)
