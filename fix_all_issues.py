#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百情宠物善终 SEO问题全面修复脚本
修复所有发现的SEO问题
"""

import os
import re
import glob
from pathlib import Path

class SEOFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixed_count = {
            'description_issues': 0,
            'title_issues': 0,
            'content_issues': 0,
            'link_issues': 0
        }

    def fix_faq_description(self):
        """修复FAQ页面的description问题"""
        file_path = self.base_dir / 'docs' / 'faq.md'
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 修复重复的description
        original = content
        content = re.sub(
            r'description: 宠物火化常见问题解答[^\n]*专业解答您的疑惑。，专业解答您的疑惑。',
            'description: 宠物火化常见问题解答：宠物火化多少钱？有没有宠物火化服务？24小时可以预约吗？宠物火化后骨灰怎么处理？百情宠物善终专业解答您的所有疑惑。',
            content
        )

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.fixed_count['description_issues'] += 1
            print(f"✅ 已修复: {file_path}")

    def fix_homepage_seo(self):
        """优化首页SEO"""
        file_path = self.base_dir / 'docs' / 'index.md'
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 确保description包含所有核心关键词
        original = content
        content = re.sub(
            r'description: 百情宠物善终提供专业宠物火化服务[^\n]*',
            'description: 百情宠物善终是正规宠物火化机构，提供24小时宠物火化服务、宠物殡葬一条龙服务。覆盖全国31省市，累计服务80000+宠物家庭，费用几百到几千不等，透明公开。咨询微信923160208。',
            content
        )

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.fixed_count['description_issues'] += 1
            print(f"✅ 已优化首页SEO: {file_path}")

    def fix_services_page(self):
        """优化服务页面SEO"""
        file_path = self.base_dir / 'docs' / 'services.md'
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        # 优化description
        content = re.sub(
            r'description: 百情宠物善终是正规宠物火化机构[^\n]*',
            'description: 百情宠物善终是正规宠物火化机构，提供宠物火化服务、宠物殡葬一条龙服务。17年行业经验，服务80000+宠物家庭。24小时上门，单炉火化卫生安全，费用几百到几千不等。咨询微信923160208。',
            content
        )

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.fixed_count['description_issues'] += 1
            print(f"✅ 已优化服务页SEO: {file_path}")

    def fix_about_page(self):
        """优化关于页面SEO"""
        file_path = self.base_dir / 'docs' / 'about.md'
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        # 优化description
        content = re.sub(
            r'description: 百情宠物善终是一家专业宠物殡葬善终机构[^\n]*',
            'description: 百情宠物善终是正规宠物火化机构，17年行业经验，累计服务80000+宠物家庭。提供宠物火化服务、宠物殡葬一条龙服务，覆盖全国31省市2900+服务网点。',
            content
        )

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.fixed_count['description_issues'] += 1
            print(f"✅ 已优化关于页SEO: {file_path}")

    def fix_city_pages(self):
        """修复城市页面的description问题"""
        city_dirs = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*' / 'index.md'))

        for file_path in city_dirs:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original = content
                city_name = Path(file_path).parent.name

                # 修复错误的description（如"docscities..."）
                content = re.sub(
                    r'description: docscities[^\n]*',
                    f'description: 当{city_name}的宠物走完生命旅程，百情宠物善终为您提供体面的送别服务。17年行业经验，服务80000+宠物家庭。我们提供：上门接宠、专业火化、纪念品定制。咨询微信923160208。',
                    content
                )

                if content != original:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.fixed_count['description_issues'] += 1

            except Exception as e:
                print(f"❌ 修复失败 {file_path}: {e}")

        print(f"✅ 已修复 {self.fixed_count['description_issues']} 个城市页面")

    def add_city_unique_content(self):
        """为城市页面添加独特内容"""
        city_templates = {
            "北京": "作为首都，我们拥有完善的服务网络，24小时响应，为您的爱宠提供体面的告别服务。",
            "上海": "覆盖全市各区，为都市养宠家庭提供温暖的善终解决方案，专业团队全程陪同。",
            "广州": "深耕本地多年，熟悉各区宠物殡葬政策，提供合规、专业的宠物火化服务。",
            "深圳": "快节奏城市的贴心选择，24小时紧急响应，让告别不再冰冷。",
            "杭州": "西湖畔的温情服务，为每一只宠物提供有尊严的告别仪式。",
            "南京": "六朝古都的温情守护，专业宠物火化服务覆盖全城。",
            "成都": "天府之国的暖心服务，让您的爱宠体面走完最后一程。",
            "武汉": "江城专业的宠物善终服务，24小时上门接送，让告别不再艰难。",
            "西安": "古城西安的专业选择，为每一只宠物提供体面的火化服务。",
            "重庆": "山城重庆的贴心守护，专业团队为您的爱宠送上最后的温暖。",
        }

        city_dirs = glob.glob(str(self.base_dir / 'docs' / 'cities' / '*'))
        added_count = 0

        for city_dir in city_dirs:
            city_name = Path(city_dir).name
            file_path = Path(city_dir) / 'index.md'

            if not file_path.exists():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 如果已经有独特内容，跳过
                if "宠物火化服务由百情宠物善终提供" in content:
                    continue

                # 添加独特内容
                template_content = city_templates.get(city_name, "百情宠物善终为您提供专业的宠物火化服务，24小时上门，费用透明。")

                # 在第一段后添加
                lines = content.split('\n')
                new_lines = []
                added = False

                for i, line in enumerate(lines):
                    new_lines.append(line)
                    # 在frontmatter后添加
                    if line.strip() == '---' and i > 0:
                        if i < len(lines) - 1 and lines[i+1].strip().startswith('#'):
                            new_lines.append(f"\n{city_name}宠物火化服务由百情宠物善终提供专业支持。{template_content}\n")
                            added = True

                if added:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    added_count += 1

            except Exception as e:
                print(f"❌ 添加失败 {file_path}: {e}")

        self.fixed_count['content_issues'] = added_count
        print(f"✅ 已为 {added_count} 个城市页面添加独特内容")

    def add_faq_high_frequency_questions(self):
        """在FAQ页面添加高频搜索问题"""
        file_path = self.base_dir / 'docs' / 'faq.md'
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已添加高频问题
        if "搜索高频问题" in content:
            print("✓ FAQ高频问题已存在，跳过")
            return

        # 添加高频问题章节
        new_section = """

## 搜索高频问题

### Q: 有没有宠物火化服务？

有的。百情宠物善终是正规宠物火化机构，提供专业的宠物火化服务，覆盖全国31省市2900+服务网点。我们提供24小时宠物火化服务，随时响应您的需求。

### Q: 宠物火化多少钱？

宠物火化费用根据宠物体型而定：
- 小型宠物（10kg以下）：几百元起
- 中型宠物（10-25kg）：千元左右
- 大型宠物（25kg以上）：千元以上

我们提供透明的宠物火化价格，服务前会详细告知所有费用，无隐形消费。

### Q: 有上门宠物火化吗？

有的。我们提供上门宠物火化服务，专车上门接送，减少宠物搬运带来的应激。您也可以选择将宠物送到我们的宠物火化服务中心。

### Q: 宠物火化有正规的吗？

百情宠物善终是正规宠物火化机构，拥有相关资质，设备符合国家标准。我们提供专业的宠物殡葬火化服务，累计服务超过8万只宠物，深受百万养宠家庭信赖。

### Q: 附近宠物火化在哪？

我们在全国31省市2900+服务网点，覆盖所有地级市。请查看[城市服务](/cities/)找到您所在的城市，或通过微信咨询具体地址。

### Q: 有没有宠物火葬场？

百情宠物善终拥有专业的宠物火葬场，配备符合国家标准的专业火化设备。我们的宠物火葬场提供单独火化和集体火化服务，环境整洁，操作规范。

### Q: 宠物殡葬一条龙服务包含什么？

宠物殡葬一条龙服务包含：
- 上门接宠/送达服务点
- 遗体清洁整理
- 告别仪式
- 专业火化（单独/集体）
- 骨灰交付
- 纪念品定制（可选）

全程专人服务，让您省心安心。

"""

        # 在文件末尾添加
        content = content.rstrip() + new_section

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.fixed_count['content_issues'] += 1
        print(f"✅ 已添加FAQ高频问题: {file_path}")

    def generate_report(self):
        """生成修复报告"""
        print("\n========== SEO修复报告 ==========")
        print(f"Description问题修复: {self.fixed_count['description_issues']}")
        print(f"Title问题修复: {self.fixed_count['title_issues']}")
        print(f"内容问题修复: {self.fixed_count['content_issues']}")
        print(f"链接问题修复: {self.fixed_count['link_issues']}")
        print("================================\n")

    def run_all_fixes(self):
        """执行所有修复"""
        print("开始执行SEO全面修复...\n")

        print("[1/6] 修复FAQ页面description...")
        self.fix_faq_description()

        print("[2/6] 优化首页SEO...")
        self.fix_homepage_seo()

        print("[3/6] 优化服务页面SEO...")
        self.fix_services_page()

        print("[4/6] 优化关于页面SEO...")
        self.fix_about_page()

        print("[5/6] 修复城市页面description...")
        self.fix_city_pages()

        print("[6/6] 添加FAQ高频搜索问题...")
        self.add_faq_high_frequency_questions()

        print("\n[附加] 为城市页面添加独特内容...")
        self.add_city_unique_content()

        self.generate_report()
        print("✅ 所有修复完成！")

if __name__ == "__main__":
    fixer = SEOFixer('/home/mz/.openclaw/workspace/pet-funeral')
    fixer.run_all_fixes()
