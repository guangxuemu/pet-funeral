#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物殡葬站点SEO优化器 v1.0
- 内链建设
- H2标签优化
- 禁用词替换
- 违规内容删除
"""

import re
from pathlib import Path
from collections import defaultdict

class SEOOptimizer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.cities_dir = self.project_dir / 'docs/cities'
        self.stats = {
            'total_articles': 0,
            'internal_links_added': 0,
            'h2_added': 0,
            'forbidden_words_fixed': 0,
            'phone_removed': 0,
            'qualification_removed': 0,
        }
        self.dry_run = True
        self.changes = []
    
    def get_all_articles(self):
        """获取所有区县文章"""
        articles = list(self.cities_dir.glob('*/*/*.md'))
        articles = [f for f in articles if f.name != 'index.md']
        self.stats['total_articles'] = len(articles)
        return articles
    
    def add_internal_links(self, content, province, city):
        """添加内链"""
        # 检查是否已有内链
        if '相关服务' in content or '**服务覆盖' in content:
            return content, False
        
        # 找到最后一个 <MyContact /> 的位置
        contact_pattern = r'(<MyContact />)'
        matches = list(re.finditer(contact_pattern, content))
        
        if len(matches) >= 2:
            # 在最后一个 MyContact 之前插入
            last_contact = matches[-1]
            insert_pos = last_contact.start()
            
            links_html = f'''
---
**服务覆盖：**
- [{city}宠物火化服务](/cities/{province}/{city}/) - 全市服务网点
- [{province}宠物火化服务](/cities/{province}/) - 全省服务覆盖

'''
            
            new_content = content[:insert_pos] + links_html + content[insert_pos:]
            return new_content, True
        
        return content, False
    
    def add_h2_tags(self, content):
        """添加H2标签"""
        modified = False
        
        # 匹配"一、二、三、四"等章节标题
        patterns = [
            (r'^一、', '## 一、'),
            (r'^二、', '## 二、'),
            (r'^三、', '## 三、'),
            (r'^四、', '## 四、'),
            (r'^五、', '## 五、'),
        ]
        
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_line = line
            for pattern, replacement in patterns:
                if re.match(pattern, line.strip()) and not line.startswith('##'):
                    new_line = line.replace(line.strip(), replacement + line.strip()[2:])
                    modified = True
                    break
            new_lines.append(new_line)
        
        return '\n'.join(new_lines), modified
    
    def fix_forbidden_words(self, content):
        """替换禁用词"""
        replacements = [
            ('正规机构', '我们'),
            ('多家机构', '我们'),
            ('处理掉', '妥善处理'),
            ('扔掉', '妥善安葬'),
            ('丢弃', '妥善安置'),
        ]
        
        modified = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True
                self.changes.append(f"  替换: '{old}' → '{new}'")
        
        return content, modified
    
    def remove_qualification_mentions(self, content):
        """删除资质相关内容"""
        patterns_to_remove = [
            r'营业执照[^\n]*',
            r'动物防疫条件合格证[^\n]*',
            r'具备相关资质[^\n]*',
            r'拥有.*资质[^\n]*',
        ]
        
        modified = False
        for pattern in patterns_to_remove:
            if re.search(pattern, content):
                content = re.sub(pattern, '', content)
                modified = True
                self.changes.append(f"  删除资质提及")
        
        # 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content, modified
    
    def remove_phone_numbers(self, content):
        """删除电话号码，只保留微信"""
        # 匹配各种电话格式
        phone_patterns = [
            r'电话[：:]\s*[\d\-]{7,}[^\n]*',
            r'Tel[：:]\s*[\d\-]{7,}[^\n]*',
            r'手机[：:]\s*[\d\-]{11}[^\n]*',
            r'热线[：:]\s*[\d\-]{7,}[^\n]*',
            r'联系电话[：:]\s*[\d\-]{7,}[^\n]*',
        ]
        
        modified = False
        for pattern in phone_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, '', content)
                modified = True
                self.changes.append(f"  删除电话号码")
        
        return content, modified
    
    def optimize_article(self, article_path, dry_run=True):
        """优化单篇文章"""
        self.dry_run = dry_run
        self.changes = []
        
        # 解析路径
        parts = str(article_path.relative_to(self.cities_dir)).split('/')
        province = parts[0]
        city = parts[1]
        
        # 读取内容
        content = article_path.read_text(encoding='utf-8')
        original_content = content
        
        # 1. 添加内链
        content, changed = self.add_internal_links(content, province, city)
        if changed:
            self.stats['internal_links_added'] += 1
            self.changes.append("  ✅ 添加内链")
        
        # 2. 添加H2标签
        content, changed = self.add_h2_tags(content)
        if changed:
            self.stats['h2_added'] += 1
            self.changes.append("  ✅ 添加H2标签")
        
        # 3. 替换禁用词
        content, changed = self.fix_forbidden_words(content)
        if changed:
            self.stats['forbidden_words_fixed'] += 1
        
        # 4. 删除资质提及
        content, changed = self.remove_qualification_mentions(content)
        if changed:
            self.stats['qualification_removed'] += 1
        
        # 5. 删除电话号码
        content, changed = self.remove_phone_numbers(content)
        if changed:
            self.stats['phone_removed'] += 1
        
        # 如果有修改且非预演模式，写入文件
        if content != original_content and not dry_run:
            article_path.write_text(content, encoding='utf-8')
            return True
        
        return content != original_content
    
    def run(self, dry_run=True):
        """运行优化器"""
        self.dry_run = dry_run
        
        print("=" * 70)
        print(f"📋 SEO优化器 - {'预演模式' if dry_run else '实际执行'}")
        print("=" * 70)
        
        articles = self.get_all_articles()
        print(f"\n总文章数: {len(articles)}")
        
        modified_count = 0
        modified_articles = []
        
        for i, article in enumerate(articles, 1):
            if i % 500 == 0:
                print(f"  处理进度: {i}/{len(articles)}")
            
            has_changes = self.optimize_article(article, dry_run)
            if has_changes:
                modified_count += 1
                modified_articles.append({
                    'path': str(article.relative_to(self.cities_dir)),
                    'changes': self.changes.copy()
                })
        
        # 输出统计
        print("\n" + "=" * 70)
        print("📊 优化统计")
        print("=" * 70)
        print(f"  处理文章: {len(articles)}")
        print(f"  需要修改: {modified_count}")
        print(f"  添加内链: {self.stats['internal_links_added']}")
        print(f"  添加H2标签: {self.stats['h2_added']}")
        print(f"  修复禁用词: {self.stats['forbidden_words_fixed']}")
        print(f"  删除资质提及: {self.stats['qualification_removed']}")
        print(f"  删除电话号码: {self.stats['phone_removed']}")
        
        return modified_articles


if __name__ == '__main__':
    import sys
    
    project_dir = Path(__file__).parent
    optimizer = SEOOptimizer(project_dir)
    
    # 默认预演模式，传入 --execute 参数实际执行
    dry_run = '--execute' not in sys.argv
    
    modified = optimizer.run(dry_run=dry_run)
    
    if dry_run and modified:
        print("\n" + "=" * 70)
        print("⚠️ 这是预演模式，未实际修改文件")
        print("确认无误后，执行: python3 seo_optimizer.py --execute")
        print("=" * 70)
