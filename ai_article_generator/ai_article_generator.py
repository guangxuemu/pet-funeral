#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物殡葬文章生成器 v8.6
标题从关键词表随机选取风格，确保多样化
"""

import os
import re
import random
import pandas as pd
import requests
from pathlib import Path
from typing import Optional, List

# ==================== 配置 ====================
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
LONGCAT_API_URL = "https://api.longcat.chat/openai/v1/chat/completions"
LONGCAT_API_KEY = "ak_2bP2XS4zs3jN4qk4kM2PM6UQ1gy10"
LONGCAT_MODEL = "LongCat-Flash-Lite"
KEYWORD_FILE = PROJECT_DIR / "宠物-关键词表.xlsx"


def load_keywords() -> dict:
    """加载关键词并分类"""
    df = pd.read_excel(KEYWORD_FILE)
    keywords = df['关键词'].dropna().tolist()
    
    return {
        'question': [k for k in keywords if '哪里' in k or '有没有' in k or '哪家' in k or '怎么' in k or '多少钱' in k or '如何' in k or '什么' in k],
        'center': [k for k in keywords if '中心' in k or '机构' in k or '服务' in k or '馆' in k or '场' in k or '公司' in k],
        'action': [k for k in keywords if '死了' in k or '去世' in k or '离世' in k or '处理' in k or '安葬' in k],
        'special': [k for k in keywords if '24小时' in k or '上门' in k or '附近' in k or '正规' in k or '专业' in k],
        'all': keywords
    }


def call_ai(prompt: str) -> Optional[str]:
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LONGCAT_API_KEY}"}
        data = {"model": LONGCAT_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.95, "max_tokens": 2500}
        resp = requests.post(LONGCAT_API_URL, headers=headers, json=data, timeout=120)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"API错误: {e}")
    return None


def build_district_prompt(district: str, modifier: str, keywords: dict) -> str:
    """区县文章提示词"""
    
    # 随机选取不同风格的关键词作为参考
    ref_keywords = []
    for style in ['question', 'center', 'action', 'special']:
        if keywords[style]:
            ref_keywords.extend(random.sample(keywords[style], min(2, len(keywords[style]))))
    
    ref_hint = "、".join(ref_keywords[:8])
    
    prompt = f"""你是宠物殡葬内容专家。为"{district}宠物火化服务"写一篇文章。

【地区】{district}（{modifier}）
【参考标题风格】{ref_hint}

【标题要求】
- 标题必须包含完整区县名称"{district}"
- 标题必须包含"宠物火化"或"宠物殡葬"或"宠物善终"
- 不要加城市名（上海）
- 参考上面的关键词风格，多样化有吸引力
- 可以是：疑问式、服务式、场景式、特色式等
- 每个区的标题风格要不一样
- 20-30字

【内容要求】
- 1200-1500字
- 温暖专业

【内容结构】直接写内容，不要章节标记

开头：2-3句情感共鸣

一、快速回答
- 服务覆盖：{district}
- 核心流程
- 费用参考
- 联系方式：微信 923160208

二、详细说明

三、温馨提示

四、常见问题

【禁止】
- 无具体价格数字
- 不用"死亡""尸体"

直接输出，标题用#开头。"""
    return prompt


def build_page(content: str) -> str:
    """构建页面"""
    
    lines = content.strip().split('\n')
    title = ""
    body_lines = []
    
    for line in lines:
        if line.startswith('#') and not title:
            title = line.strip()
            if not title.startswith('# '):
                title = '# ' + title.lstrip('#').strip()
        else:
            body_lines.append(line)
    
    # 标题清理
    title = title.replace('死亡', '离开').replace('尸体', '遗体')
    
    body = '\n'.join(body_lines).strip()
    
    # 清理
    body = body.replace('死亡', '离开').replace('尸体', '遗体')
    body = re.sub(r'(\d{2,})元', '几百到几千不等', body)
    body = re.sub(r'92[0-9]{8}', '923160208', body)
    body = re.sub(r'###?\s*情感开头\s*\n*', '', body)
    body = re.sub(r'###?\s*开头段落\s*\n*', '', body)
    
    return f"""{title}

<Breadcrumb />

<DistrictList />

<MyContact />

{body}

<MyContact />
"""


# 城市配置
CITIES = {
    "上海": {
        "province": "上海",
        "city": "上海",
        "districts": [
            ("黄浦区", "市中心核心商圈"),
            ("徐汇区", "教育文化高地"),
            ("长宁区", "国际社区"),
            ("静安区", "商务精英聚集地"),
            ("普陀区", "西部宜居新城"),
            ("虹口区", "北部人文荟萃"),
            ("杨浦区", "高校科创中心"),
            ("闵行区", "南部新兴城区"),
            ("宝山区", "北部工业重镇"),
            ("嘉定区", "西北汽车城"),
            ("浦东新区", "改革开放前沿"),
            ("金山区", "西南滨海新城"),
            ("松江区", "上海之根文化古城"),
            ("青浦区", "西大门江南水乡"),
            ("奉贤区", "南郊生态新城"),
            ("崇明区", "生态岛屿后花园"),
        ]
    },
    "南京": {
        "province": "江苏",
        "city": "南京",
        "districts": [
            ("玄武区", "历史文化核心"),
            ("秦淮区", "古都风韵城区"),
            ("建邺区", "现代化新中心"),
            ("鼓楼区", "教育文化中心"),
            ("浦口区", "江北新区门户"),
            ("栖霞区", "东部科教新城"),
            ("雨花台区", "软件产业高地"),
            ("江宁区", "南部综合新城"),
            ("六合区", "北部生态区域"),
            ("溧水区", "南部宜居新城"),
            ("高淳区", "国际慢城"),
        ]
    }
}


def generate_city(city_name: str):
    """生成指定城市的区县文章"""
    if city_name not in CITIES:
        print(f"❌ 未知城市: {city_name}")
        return
    
    config = CITIES[city_name]
    keywords = load_keywords()
    
    output_dir = PROJECT_DIR / "docs/cities" / config["province"] / config["city"]
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print(f"生成 {city_name} 区县文章")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for district, modifier in config["districts"]:
        output_file = output_dir / f"{district}宠物火化服务.md"
        
        # 跳过已存在的文件
        if output_file.exists():
            print(f"⏭️ {district}: 已存在，跳过")
            continue
        
        prompt = build_district_prompt(district, modifier, keywords)
        content = call_ai(prompt)
        
        if content:
            page = build_page(content)
            output_file.write_text(page, encoding='utf-8')
            title = page.split('\n')[0]
            print(f"✅ {district}: {title}")
            success += 1
        else:
            print(f"❌ {district}: 失败")
            failed += 1
    
    print("=" * 60)
    print(f"完成: 成功 {success}, 失败 {failed}")


def main():
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "上海"
    generate_city(city)


if __name__ == "__main__":
    main()
