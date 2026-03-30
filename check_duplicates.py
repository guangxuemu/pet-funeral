#!/usr/bin/env python3
"""
检查站点重复内容、链接和title/H1不一致
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def get_all_md_files(docs_dir):
    """获取所有markdown文件"""
    return list(Path(docs_dir).rglob('*.md'))

def check_duplicate_titles(files):
    """检查重复title"""
    titles = defaultdict(list)
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                if match:
                    title = match.group(1).strip().strip('"\'')
                    titles[title].append(str(f))
        except:
            pass
    
    duplicates = {k: v for k, v in titles.items() if len(v) > 1}
    return duplicates

def check_title_h1_mismatch(files):
    """检查title和H1不一致"""
    mismatches = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 提取frontmatter title
            title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            # 提取H1标题
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            
            if title_match and h1_match:
                title = title_match.group(1).strip().strip('"\'')
                h1 = h1_match.group(1).strip()
                
                # 清理后进行比较
                title_clean = re.sub(r'\s*[-|]\s*.*$', '', title).strip()
                h1_clean = re.sub(r'\s*[-|]\s*.*$', '', h1).strip()
                
                if title_clean != h1_clean and abs(len(title) - len(h1)) > 5:
                    mismatches.append({
                        'file': str(f),
                        'title': title,
                        'h1': h1
                    })
        except:
            pass
    
    return mismatches

def check_internal_links(files):
    """检查内部链接"""
    all_links = defaultdict(list)
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 提取所有链接 [text](/path)
            links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
            for text, link in links:
                all_links[link].append(str(f))
        except:
            pass
    
    return all_links

def check_description_issues(files):
    """检查description问题"""
    issues = {
        'too_short': [],
        'too_long': [],
        'missing': []
    }
    
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                
            desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
            if desc_match:
                desc = desc_match.group(1).strip().strip('"\'')
                desc_len = len(desc)
                
                if desc_len < 50:
                    issues['too_short'].append({'file': str(f), 'len': desc_len, 'desc': desc[:50]})
                elif desc_len > 160:
                    issues['too_long'].append({'file': str(f), 'len': desc_len, 'desc': desc[:80]})
            else:
                issues['missing'].append(str(f))
        except:
            pass
    
    return issues

def main():
    docs_dir = '/home/mz/.openclaw/workspace/pet-funeral/docs'
    files = get_all_md_files(docs_dir)
    
    print(f"总文件数: {len(files)}")
    print("=" * 60)
    
    # 检查重复title
    print("\n【重复Title检查】")
    duplicates = check_duplicate_titles(files)
    if duplicates:
        print(f"发现 {len(duplicates)} 个重复title:")
        for title, files_list in list(duplicates.items())[:10]:
            print(f"  • '{title[:50]}...' 出现在 {len(files_list)} 个文件")
    else:
        print("✅ 未发现重复title")
    
    # 检查title/H1不一致
    print("\n【Title/H1不一致检查】")
    mismatches = check_title_h1_mismatch(files)
    print(f"发现 {len(mismatches)} 个不一致")
    if mismatches:
        print("前10个示例:")
        for m in mismatches[:10]:
            print(f"  文件: {m['file']}")
            print(f"    title: {m['title'][:50]}...")
            print(f"    H1: {m['h1'][:50]}...")
            print()
    
    # 检查内部链接
    print("\n【内部链接统计】")
    links = check_internal_links(files)
    print(f"总链接数: {len(links)}")
    
    # 检查description问题
    print("\n【Description检查】")
    desc_issues = check_description_issues(files)
    print(f"  过短(<50字符): {len(desc_issues['too_short'])} 个")
    print(f"  过长(>160字符): {len(desc_issues['too_long'])} 个")
    print(f"  缺失: {len(desc_issues['missing'])} 个")
    
    if desc_issues['too_short']:
        print("\n  过短示例:")
        for item in desc_issues['too_short'][:5]:
            print(f"    • {item['file']}: {item['len']}字符")
    
    print("\n" + "=" * 60)
    print("检查完成!")

if __name__ == '__main__':
    main()
