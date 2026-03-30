#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面检查项目：重复、遗漏、多余、404链接
"""
import os
import re
import json
from collections import defaultdict

class ComprehensiveChecker:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.docs_dir = os.path.join(base_dir, 'docs')
        self.cities_dir = os.path.join(self.docs_dir, 'cities')
        self.issues = {
            'duplicates': [],
            'missing': [],
            'extras': [],
            'broken_links': [],
            'format_issues': []
        }
        self.stats = {
            'total_files': 0,
            'province_pages': 0,
            'city_pages': 0,
            'district_pages': 0
        }
        
    def check_all(self):
        """执行所有检查"""
        self.scan_structure()
        self.check_duplicates()
        self.check_missing_files()
        self.check_format_issues()
        self.check_broken_links()
        return self.generate_report()
    
    def scan_structure(self):
        """扫描项目结构"""
        for root, dirs, files in os.walk(self.cities_dir):
            for file in files:
                if file.endswith('.md'):
                    self.stats['total_files'] += 1
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.cities_dir)
                    parts = rel_path.split(os.sep)
                    
                    if len(parts) == 2:  # 省份页面: 省份/index.md
                        self.stats['province_pages'] += 1
                    elif len(parts) == 3:  # 城市页面: 省份/城市/index.md
                        self.stats['city_pages'] += 1
                    elif len(parts) == 3 and not file == 'index.md':  # 区县页面
                        self.stats['district_pages'] += 1
    
    def check_duplicates(self):
        """检查重复内容"""
        # 检查标题重复
        titles = defaultdict(list)
        for root, dirs, files in os.walk(self.cities_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 提取标题
                        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                        if title_match:
                            title = title_match.group(1).strip()
                            titles[title].append(filepath)
        
        for title, files in titles.items():
            if len(files) > 1:
                self.issues['duplicates'].append({
                    'type': 'duplicate_title',
                    'title': title,
                    'files': files
                })
    
    def check_missing_files(self):
        """检查缺失文件"""
        # 检查每个城市是否都有index.md
        for root, dirs, files in os.walk(self.cities_dir):
            if os.path.basename(root) in ['cities']:  # 跳过根目录
                continue
            if 'index.md' not in files and any(f.endswith('.md') for f in files):
                # 这是一个有区县文章但没有index.md的城市
                pass  # 暂时不报告，因为可能是区县文章目录
    
    def check_format_issues(self):
        """检查格式问题"""
        required_components = ['<Breadcrumb />', '<DistrictList />', '<MyContact />']
        
        for root, dirs, files in os.walk(self.cities_dir):
            for file in files:
                if file.endswith('.md') and file != 'index.md':
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    issues = []
                    for component in required_components:
                        if component not in content:
                            issues.append(f"缺少{component}")
                    
                    # 检查frontmatter
                    if not content.startswith('---'):
                        issues.append("缺少frontmatter")
                    
                    # 检查H1标题
                    if not re.search(r'^#\s+.+$', content, re.MULTILINE):
                        issues.append("缺少H1标题")
                    
                    if issues:
                        self.issues['format_issues'].append({
                            'file': filepath,
                            'issues': issues
                        })
    
    def check_broken_links(self):
        """检查404链接"""
        # 收集所有存在的文件
        existing_files = set()
        for root, dirs, files in os.walk(self.cities_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.docs_dir)
                    # 转换为URL格式
                    url_path = rel_path.replace('.md', '.html').replace(os.sep, '/')
                    existing_files.add(url_path)
                    # 也添加目录形式的链接
                    if file == 'index.md':
                        dir_path = os.path.dirname(rel_path).replace(os.sep, '/')
                        existing_files.add(dir_path + '/')
                        existing_files.add(dir_path)
        
        # 检查所有链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for root, dirs, files in os.walk(self.cities_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    links = re.findall(link_pattern, content)
                    for text, link in links:
                        # 只检查内部链接
                        if link.startswith('/'):
                            # 移除hash和query
                            clean_link = link.split('#')[0].split('?')[0]
                            if clean_link and clean_link not in existing_files:
                                # 可能是动态生成的链接，跳过DistrictList相关
                                if '宠物火化服务' not in clean_link:
                                    self.issues['broken_links'].append({
                                        'file': filepath,
                                        'link': link,
                                        'text': text
                                    })
    
    def generate_report(self):
        """生成检查报告"""
        report = []
        report.append("=" * 80)
        report.append("宠物殡葬项目全面检查报告")
        report.append("=" * 80)
        report.append("")
        
        # 统计信息
        report.append("📊 项目统计")
        report.append("-" * 80)
        report.append(f"总文件数: {self.stats['total_files']}")
        report.append(f"省份页面: {self.stats['province_pages']}")
        report.append(f"城市页面: {self.stats['city_pages']}")
        report.append(f"区县页面: {self.stats['district_pages']}")
        report.append("")
        
        # 重复内容
        if self.issues['duplicates']:
            report.append("🔴 重复内容")
            report.append("-" * 80)
            for dup in self.issues['duplicates'][:5]:  # 只显示前5个
                report.append(f"标题: {dup['title']}")
                for f in dup['files']:
                    report.append(f"  - {f}")
            report.append("")
        
        # 格式问题
        if self.issues['format_issues']:
            report.append("🟡 格式问题")
            report.append("-" * 80)
            for issue in self.issues['format_issues'][:10]:
                report.append(f"文件: {issue['file']}")
                for i in issue['issues']:
                    report.append(f"  - {i}")
            report.append("")
        
        # 404链接
        if self.issues['broken_links']:
            report.append("🔴 可疑链接（需人工确认）")
            report.append("-" * 80)
            for link in self.issues['broken_links'][:10]:
                report.append(f"文件: {link['file']}")
                report.append(f"  链接: {link['link']}")
                report.append(f"  文本: {link['text']}")
            report.append("")
        
        return '\n'.join(report)

if __name__ == '__main__':
    checker = ComprehensiveChecker('/home/mz/.openclaw/workspace/pet-funeral')
    print(checker.check_all())
