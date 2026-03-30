#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理所有360+地级城市的SEO优化
- 为每个城市添加独特内容
- 融入"宠物火葬"关键词
"""

import os
import glob
import random
from pathlib import Path

class AllCitiesOptimizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'added_content': 0,
            'added_huozang': 0
        }
        
        # 城市特色描述模板（按地域分类）
        self.region_templates = {
            '华北': [
                "作为华北地区的重要城市，我们提供专业的宠物火化服务，24小时响应。",
                "华北地区的宠物善终服务首选，专业团队为您的爱宠送上最后的温暖。",
                "深耕本地多年，为华北地区养宠家庭提供体面的宠物告别服务。",
            ],
            '华东': [
                "华东地区专业的宠物善终服务机构，服务网络覆盖全市各区。",
                "长三角地区的温情守护，专业宠物火化服务深受养宠家庭信赖。",
                "华东名城的专业选择，为您的爱宠提供有尊严的告别仪式。",
            ],
            '华南': [
                "华南地区的贴心选择，24小时紧急响应，让告别不再冰冷。",
                "珠三角专业的宠物善终服务，上门接送更省心。",
                "华南名城的温情守护，尊重每一个生命。",
            ],
            '华中': [
                "华中地区的专业宠物火化服务，覆盖全市，随时响应。",
                "中部崛起的温情守护，为华中养宠家庭提供体面的送别服务。",
                "华中名城的贴心选择，专业团队全程陪同。",
            ],
            '西南': [
                "西南地区的专业宠物善终服务，让您的爱宠体面走完最后一程。",
                "西南名城的温情守护，尊重每一份情感。",
                "深耕西南地区多年，提供合规、专业的宠物火化服务。",
            ],
            '西北': [
                "西北地区的专业选择，为每一只宠物提供体面的火化服务。",
                "西北名城的温情守护，24小时为您服务。",
                "大西北的暖心服务，专业团队为您的爱宠送上最后的温暖。",
            ],
            '东北': [
                "东北老工业基地的温情转型，专业宠物火化服务值得信赖。",
                "东北地区的暖心守护，让告别不再艰难。",
                "东北名城的贴心选择，尊重每一个生命。",
            ],
        }
        
        # 省份到地域的映射
        self.province_to_region = {
            '北京': '华北', '天津': '华北', '河北': '华北', '山西': '华北', '内蒙古': '华北',
            '上海': '华东', '江苏': '华东', '浙江': '华东', '安徽': '华东', '福建': '华东', '江西': '华东', '山东': '华东',
            '广东': '华南', '广西': '华南', '海南': '华南',
            '河南': '华中', '湖北': '华中', '湖南': '华中',
            '四川': '西南', '贵州': '西南', '云南': '西南', '西藏': '西南', '重庆': '西南',
            '陕西': '西北', '甘肃': '西北', '青海': '西北', '宁夏': '西北', '新疆': '西北',
            '辽宁': '东北', '吉林': '东北', '黑龙江': '东北',
        }
    
    def get_city_template(self, city_name, province_name):
        """根据城市和省份生成独特内容"""
        region = self.province_to_region.get(province_name, '全国')
        templates = self.region_templates.get(region, self.region_templates['华北'])
        return random.choice(templates)
    
    def optimize_city_file(self, file_path, city_name, province_name):
        """优化单个城市文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 1. 添加城市独特内容（如果还没有）
            if "宠物火化服务由百情宠物善终提供" not in content:
                template = self.get_city_template(city_name, province_name)
                
                # 在frontmatter后添加
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.strip() == '---' and i > 0:
                        if i < len(lines) - 1 and lines[i+1].strip().startswith('#'):
                            unique_content = f"\n{city_name}宠物{self.get_random_service_word()}由百情宠物善终提供专业支持。{template}\n"
                            new_lines.append(unique_content)
                            modified = True
                            self.stats['added_content'] += 1
                
                if modified:
                    content = '\n'.join(new_lines)
            
            # 2. 融入"宠物火葬"关键词
            if '宠物火葬' not in content:
                # 在适当位置添加"宠物火葬"
                if '单独火化' in content:
                    content = content.replace(
                        '单独火化',
                        '单独宠物火葬',
                        1
                    )
                    self.stats['added_huozang'] += 1
                    modified = True
            
            # 3. 保存修改
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ 失败 {file_path}: {e}")
            return False
    
    def get_random_service_word(self):
        """随机获取服务描述词"""
        words = ['火化服务', '殡葬服务', '善终服务', '告别服务', '火化殡葬']
        return random.choice(words)
    
    def run(self):
        """执行优化"""
        # 查找所有城市目录下的index.md（不包括省份级别的）
        city_files = []
        
        for province_dir in self.base_dir.glob('docs/cities/*'):
            if not province_dir.is_dir():
                continue
            province_name = province_dir.name
            
            for city_dir in province_dir.glob('*'):
                if not city_dir.is_dir():
                    continue
                city_name = city_dir.name
                index_file = city_dir / 'index.md'
                
                if index_file.exists() and city_name != 'index.md':
                    city_files.append((index_file, city_name, province_name))
        
        print(f"发现 {len(city_files)} 个地级城市页面")
        print("开始批量优化...\n")
        
        for idx, (file_path, city_name, province_name) in enumerate(sorted(city_files)):
            if len(city_name) > 10 or '/' in city_name:  # 跳过可能是文件名的
                continue
            
            # 每处理50个显示一次进度
            if idx % 50 == 0 and idx > 0:
                print(f"  ... 已处理 {idx}/{len(city_files)} 个城市")
            
            if self.optimize_city_file(file_path, city_name, province_name):
                print(f"✅ 已优化: {province_name}/{city_name}")
                self.stats['processed'] += 1
            else:
                self.stats['skipped'] += 1
        
        self.print_report()
    
    def print_report(self):
        """打印报告"""
        print("\n" + "="*60)
        print("全量城市页面优化完成报告")
        print("="*60)
        print(f"优化城市数: {self.stats['processed']}")
        print(f"添加独特内容: {self.stats['added_content']}")
        print(f"融入火葬关键词: {self.stats['added_huozang']}")
        print(f"跳过/已优化: {self.stats['skipped']}")
        print("="*60)

if __name__ == "__main__":
    optimizer = AllCitiesOptimizer('/home/mz/.openclaw/workspace/pet-funeral')
    optimizer.run()
