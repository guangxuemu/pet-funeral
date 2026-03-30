# 宠物殡葬站点 SEO 优化指南

## 站点信息

- **项目路径**: `/home/.openclaw/workspace/pet-funeral/`
- **开发服务**: `npm run docs:dev` (端口 5000)
- **生产构建**: `npm run docs:build`
- **输出目录**: `docs/.vitepress/dist/`

---

## 页面模板

### 1. 主要页面 Frontmatter

```markdown
---
title: 页面标题 - 宠物殡葬服务
description: 页面描述，150-160字符，包含关键词。
keywords: [关键词1, 关键词2, 关键词3]
---

# 页面标题

<Breadcrumb />

页面内容...
```

### 2. 城市页面模板

```markdown
---
title: {城市}宠物火化服务 - 百情宠物善终
description: {城市}宠物火化服务，百情宠物善终提供专业宠物殡葬、告别仪式、骨灰纪念等一站式服务，24小时在线，费用透明。
keywords: [{城市}宠物火化, {城市}宠物殡葬, {城市}宠物安葬]
---

# {城市}宠物火化服务

<Breadcrumb />

<MyContact />

内容...
```

### 3. 省份页面模板

```markdown
---
title: {省份}宠物火化服务 - 百情宠物善终
description: {省份}宠物火化服务网点覆盖全省各城市，提供专业宠物殡葬、告别仪式、骨灰纪念等一站式服务，24小时在线。
keywords: [{省份}宠物火化, {省份}宠物殡葬, {省份}宠物安葬]
---

# {省份}宠物火化服务

<Breadcrumb />

覆盖{N}个城市

[城市1](./城市1/) | [城市2](./城市2/) | ...
```

---

## SEO 组件

### MyContact - 微信复制组件

```vue
<MyContact />
```

功能：点击复制微信号 `923160208`

### Breadcrumb - 面包屑导航

```vue
<Breadcrumb />
```

自动生成层级导航，支持 Schema.org 结构化数据。

---

## 配置文件

### config.mts SEO 配置

```typescript
head: [
  // 基础 SEO
  ['meta', { name: 'keywords', content: '宠物殡葬,宠物火化,宠物安葬,宠物告别,宠物纪念品,宠物骨灰' }],
  ['meta', { name: 'author', content: '宠物殡葬服务' }],
  ['meta', { name: 'robots', content: 'index, follow' }],
  ['meta', { name: 'googlebot', content: 'index, follow' }],
  ['meta', { name: 'baiduspider', content: 'index, follow' }],
  
  // Open Graph
  ['meta', { property: 'og:type', content: 'website' }],
  ['meta', { property: 'og:site_name', content: '宠物殡葬服务' }],
  ['meta', { property: 'og:locale', content: 'zh_CN' }],
  ['meta', { property: 'og:image', content: 'https://www.petfuneral.cn/logo.png' }],
  
  // Twitter Card
  ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
  ['meta', { name: 'twitter:site', content: '百情宠物善终' }],
  
  // 移动端优化
  ['meta', { name: 'format-detection', content: 'telephone=no' }],
  ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
  
  // 规范链接
  ['link', { rel: 'canonical', href: 'https://www.petfuneral.cn/' }],
],
```

---

## 生成新城市页面的 Python 脚本

```python
import os

def create_city_page(region, province, city):
    """创建城市页面"""
    
    # 目录结构
    dir_path = f"docs/cities/{region}/{province}/{city}"
    os.makedirs(dir_path, exist_ok=True)
    
    # 页面内容
    content = f'''---
title: {city}宠物火化服务 - 百情宠物善终
description: {city}宠物火化服务，百情宠物善终提供专业宠物殡葬、告别仪式、骨灰纪念等一站式服务，24小时在线，费用透明。
keywords: [{city}宠物火化, {city}宠物殡葬, {city}宠物安葬]
---

# {city}宠物火化服务

<Breadcrumb />

<MyContact />

## 服务介绍

百情宠物善终在{city}提供专业宠物殡葬服务，包括：

- **单独火化**：一宠一炉，全程陪同
- **集体火化**：多宠共炉，费用更低
- **上门服务**：专车接送，减少应激
- **纪念品**：骨灰盒、晶石、吊坠等

## 服务流程

1. 预约咨询
2. 上门接送
3. 告别仪式
4. 火化服务
5. 骨灰寄送

## 联系方式

<MyContact />

- ⏰ **服务时间**：24小时全天候
'''
    
    # 写入文件
    with open(f"{dir_path}/index.md", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已创建: {dir_path}/index.md")

# 使用示例
create_city_page("huadong", "江苏", "苏州")
```

---

## 批量添加 Frontmatter 脚本

```python
import os
import re

def add_frontmatter_to_cities():
    """为所有城市页面添加 frontmatter"""
    
    for root, dirs, files in os.walk("docs/cities"):
        if "index.md" in files:
            filepath = os.path.join(root, "index.md")
            parts = root.split(os.sep)
            
            # 城市页面 (docs/cities/大区/省份/城市/index.md)
            if len(parts) >= 5:
                city = parts[4]
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否已有frontmatter
                if content.startswith('---'):
                    continue
                
                # 提取原标题
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else f"{city}宠物火化服务"
                
                # 创建frontmatter
                frontmatter = f'''---
title: {title}
description: {city}宠物火化服务，百情宠物善终提供专业宠物殡葬、告别仪式、骨灰纪念等一站式服务，24小时在线，费用透明。
keywords: [{city}宠物火化, {city}宠物殡葬, {city}宠物安葬]
---

'''
                
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter + content)

    print("Frontmatter 添加完成")
```

---

## 批量添加面包屑脚本

```python
import os

def add_breadcrumb_to_pages():
    """为所有页面添加面包屑"""
    
    count = 0
    for root, dirs, files in os.walk("docs/cities"):
        if "index.md" in files:
            filepath = os.path.join(root, "index.md")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 找到标题行并在其后添加面包屑
            new_lines = []
            added = False
            for line in lines:
                new_lines.append(line)
                if line.startswith('# ') and not added:
                    new_lines.append('\n<Breadcrumb />\n')
                    added = True
            
            if added:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                count += 1

    print(f"已为 {count} 个页面添加面包屑")
```

---

## 生成 Sitemap 脚本

```python
import os
from datetime import datetime

def generate_sitemap():
    """生成 sitemap.xml"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    pages = []
    
    # 首页
    pages.append({
        'url': 'https://www.petfuneral.cn/',
        'priority': '1.0',
        'changefreq': 'daily'
    })
    
    # 主要页面
    for p in ['services', 'faq', 'about', 'memorial']:
        pages.append({
            'url': f'https://www.petfuneral.cn/{p}.html',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 城市页面
    for root, dirs, files in os.walk('docs/cities'):
        if 'index.md' in files:
            parts = root.split(os.sep)
            if len(parts) >= 4:
                path = root.replace('docs/', '')
                priority = '0.7' if len(parts) == 4 else '0.6'
                pages.append({
                    'url': f'https://www.petfuneral.cn/{path}/',
                    'priority': priority,
                    'changefreq': 'monthly'
                })
    
    # 生成 XML
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    for p in pages:
        xml += f'''
  <url>
    <loc>{p['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{p['changefreq']}</changefreq>
    <priority>{p['priority']}</priority>
  </url>'''
    
    xml += '\n</urlset>\n'
    
    with open('docs/public/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"Sitemap 已生成，包含 {len(pages)} 个页面")
```

---

## 目录结构

```
docs/
├── index.md              # 首页
├── services.md           # 服务介绍
├── faq.md               # 常见问题
├── about.md             # 关于我们
├── memorial.md          # 纪念品
├── public/
│   ├── logo.png         # 网站Logo
│   ├── robots.txt       # 爬虫规则
│   └── sitemap.xml      # 站点地图
├── cities/
│   ├── index.md         # 城市服务首页
│   ├── huadong/         # 华东
│   │   ├── index.md
│   │   ├── 安徽/
│   │   │   ├── index.md
│   │   │   └── 合肥/index.md
│   │   └── ...
│   └── ...
└── .vitepress/
    ├── config.mts       # VitePress 配置
    └── theme/
        ├── index.ts     # 主题入口
        ├── custom.css   # 自定义样式
        ├── MyContact.vue    # 微信复制组件
        └── Breadcrumb.vue   # 面包屑组件
```

---

## SEO 检查清单

- [ ] 每页有独立的 title（50-60字符）
- [ ] 每页有独立的 description（150-160字符）
- [ ] 每页有 keywords
- [ ] robots.txt 存在
- [ ] sitemap.xml 存在并提交
- [ ] 所有内部链接可点击
- [ ] 面包屑导航存在
- [ ] 图片有 alt 属性
- [ ] 移动端适配正常
- [ ] 页面加载速度 < 3秒

---

## 搜索引擎提交

### 百度
1. 访问 https://ziyuan.baidu.com/
2. 添加网站并验证
3. 提交 sitemap.xml

### Google
1. 访问 https://search.google.com/search-console
2. 添加网站并验证
3. 提交 sitemap.xml

### 必应
1. 访问 https://www.bing.com/webmasters
2. 添加网站并验证
3. 提交 sitemap.xml

---

*最后更新: 2026-03-13*