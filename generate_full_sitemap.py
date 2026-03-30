#!/usr/bin/env python3
"""生成完整的Sitemap，包含所有省份/城市/区县页面"""

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_sitemap():
    """生成完整Sitemap"""
    
    hostname = 'https://www.cwbzxxw.com'
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = []
    
    # 1. 添加首页
    urls.append({
        'loc': f'{hostname}/',
        'priority': '1.0',
        'changefreq': 'daily'
    })
    
    # 2. 添加主要页面
    main_pages = ['services', 'faq', 'about', 'memorial', 'posts/北京宠物火化服务']
    for page in main_pages:
        urls.append({
            'loc': f'{hostname}/{page}.html',
            'priority': '0.9',
            'changefreq': 'monthly'
        })
    
    # 3. 添加城市页面
    docs_dir = 'docs/cities'
    
    for root, dirs, files in os.walk(docs_dir):
        # 计算相对路径
        rel_path = root.replace('docs/', '').replace('\\', '/')
        
        # 添加index.md页面
        if 'index.md' in files:
            parts = rel_path.split('/')
            if len(parts) == 2:  # 省份页面 /cities/省份/
                priority = '0.8'
            elif len(parts) == 3:  # 城市页面 /cities/省份/城市/
                priority = '0.7'
            else:
                priority = '0.6'
            
            urls.append({
                'loc': f'{hostname}/{rel_path}/',
                'priority': priority,
                'changefreq': 'monthly'
            })
        
        # 添加区县文章页面
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                article_path = os.path.join(rel_path, file).replace('.md', '')
                urls.append({
                    'loc': f'{hostname}/{article_path}.html',
                    'priority': '0.6',
                    'changefreq': 'monthly'
                })
    
    # 4. 生成XML
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for url_data in urls:
        url_elem = SubElement(urlset, 'url')
        
        loc = SubElement(url_elem, 'loc')
        loc.text = url_data['loc']
        
        lastmod = SubElement(url_elem, 'lastmod')
        lastmod.text = today
        
        changefreq = SubElement(url_elem, 'changefreq')
        changefreq.text = url_data['changefreq']
        
        priority = SubElement(url_elem, 'priority')
        priority.text = url_data['priority']
    
    # 格式化XML
    rough_string = tostring(urlset, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # 保存文件
    with open('docs/public/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"Sitemap生成完成！")
    print(f"总URL数: {len(urls)}")
    print(f"首页: 1个")
    print(f"主要页面: {len(main_pages)}个")
    print(f"省份页面: {len([u for u in urls if '/cities/' in u['loc'] and u['loc'].count('/') == 4])}个")
    print(f"城市页面: {len([u for u in urls if '/cities/' in u['loc'] and u['loc'].count('/') == 5])}个")
    print(f"区县文章: {len([u for u in urls if '/cities/' in u['loc'] and '.html' in u['loc']])}个")

if __name__ == '__main__':
    generate_sitemap()
