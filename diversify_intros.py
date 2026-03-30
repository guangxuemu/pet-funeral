#!/usr/bin/env python3
"""
优化文章开头，避免雷同
提供多种不同风格的开头模板
"""

import os
import re
import random

# 多样化开头模板（按风格分类）- 改进版
INTRO_TEMPLATES = [
    # 风格1：情感共鸣型（通用）
    "{city}的四季轮回中，总有些离别让人猝不及防。当{city}{district}的街头巷尾再也听不到那声熟悉的呼唤，当家门口不再有那个{action}的身影，我们才猛然意识到——那些曾经习以为常的陪伴，早已成为生命中最珍贵的记忆。",

    # 风格2：回忆叙事型
    "在{city}{district}，有多少个清晨曾被一声温柔的{sound}唤醒？有多少个黄昏曾与那个{pet_feature}的小家伙一同{scene}？{time}的朝夕相处，{pet_type}早已成为家人。如今面对离别，我们总想为它做些什么。",

    # 风格3：温情守护型
    "{city}{district}的{season}，{weather}。那个曾{action}的小生命，用{pet_feature}的陪伴温暖了{time}。当它离去，除了不舍，我们更希望能给它一个体面的告别，让这份爱在{city}的某个角落继续延续。",

    # 风格4：哲理思考型
    "有人说，养宠物就是埋下了一颗悲伤的种子。在{city}{district}，无数家庭正在经历这样的时刻——那个曾带来无数欢笑的小家伙，走到了生命的终点。如何让这份陪伴有始有终，成为每位饲主心中的牵挂。",

    # 风格5：直击痛点型
    "当{city}{district}的家中突然少了那个{action}的身影，当{scene}里再也看不到它{pet_feature}的模样，许多主人除了悲痛，更感到茫然：在这座城市里，该如何妥善安排爱宠的后事？",

    # 风格6：记忆珍藏型
    "{memory}。在{city}{district}，{pet_type}用{time}的陪伴，为主人编织了无数温暖的回忆。{city}的{scene}依旧，只是身边少了那个熟悉的身影。面对离别，我们需要一种更有尊严的方式来珍藏这份爱。",

    # 风格7：场景代入型
    "走在{city}{district}的{scene}，你是否也曾想起那个{action}的小家伙？{time}的陪伴，它早已成为你生命中不可分割的一部分。当它离去，如何让这份陪伴画上圆满的句号，是我们都需要思考的问题。",

    # 风格8：温情告别型
    "每一个生命都值得被尊重，每一场陪伴都应当有始有终。在{city}{district}，越来越多的饲主开始意识到——为离世的爱宠安排一场温暖的告别，不仅是对它的尊重，更是对自己情感的一种安放。",

    # 风格9：城市特色型
    "{city}这座城市的每个角落，都承载着无数人与宠物的故事。在{district}，那个曾{action}的小生命，用{pet_feature}的陪伴温暖了主人的{time}。如今它离去，我们希望能用最温柔的方式，送它最后一程。",

    # 风格10：情感疗愈型
    "失去{city}{district}家中那个{action}的小家伙，那种痛楚难以言喻。{memory}。面对离别，我们需要的不仅是妥善处理的方式，更是一份理解与支持，让这场告别成为情感疗愈的开始。",
]

# 可替换的变量
VARIABLES = {
    'season': ['春天', '夏天', '秋天', '冬天', '清晨', '黄昏'],
    'action': ['摇着尾巴迎接你回家', '撒娇卖萌', '静静守候', '欢快奔跑', '温柔陪伴'],
    'scene': ['街头巷尾', '公园长椅', '阳台角落', '小区花园', '窗前阳光下'],
    'sound': ['叫声', '呼噜声', '脚步声', '撒娇声'],
    'time': ['数年', '十几年', '一千多个日夜', '无数个朝夕'],
    'pet_type': ['毛孩子', '小主子', '毛茸茸的家人', '陪伴多年的伙伴'],
    'memory': ['那些温暖的日子，如今想来依然心头一热', '那些共同走过的岁月，成为生命中最柔软的角落', '那份毫无保留的爱，至今仍温暖着主人的心'],
    'pet_feature': ['忠诚', '温柔', '活泼', '乖巧', '懂事'],
    'weather': ['阳光正好', '微风轻拂', '细雨绵绵', '落叶飘零'],
}

def generate_intro(district, city, province):
    """生成随机开头"""
    template = random.choice(INTRO_TEMPLATES)
    
    # 替换变量
    result = template.format(
        district=district,
        city=city,
        province=province,
        season=random.choice(VARIABLES['season']),
        action=random.choice(VARIABLES['action']),
        scene=random.choice(VARIABLES['scene']),
        sound=random.choice(VARIABLES['sound']),
        time=random.choice(VARIABLES['time']),
        pet_type=random.choice(VARIABLES['pet_type']),
        memory=random.choice(VARIABLES['memory']),
        pet_feature=random.choice(VARIABLES['pet_feature']),
        weather=random.choice(VARIABLES['weather']),
    )
    
    return result

def fix_article_intro(filepath, province, city, district):
    """修复单篇文章的开头"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 找到正文开头（DistrictList之后，第一个##之前）
        # 尝试多种模式
        patterns = [
            r'(<DistrictList />\n\n\n+)(.*?)(\n\n---)',  # 有---分隔
            r'(<DistrictList />\n\n\n+)(.*?)(\n##)',     # 直接到##
            r'(<Breadcrumb />\n\n<DistrictList />\n\n\n+)(.*?)(\n\n---)',  # 带Breadcrumb
            r'(<DistrictList />\n\n+)(.*?)(\n## [一二三四五])',  # 中文序号
        ]
        
        old_intro = None
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                old_intro = match.group(2).strip()
                break
        
        if not old_intro:
            return False
        
        # 检查是否是需要优化的雷同开头（更宽松的匹配）
        cliched_patterns = [
            r'当.*?毛孩子',
            r'当.*?陪伴.*?年',
            r'当.*?爱宠.*?离开',
            r'当.*?生命.*?终点',
            r'每一个.*?生命.*?陪伴',
            r'有人说.*?生命太短',
            r'失去.*?陪伴',
            r'还记得.*?那个',
            r'.*?的.*?，.*?当.*?',
        ]
        
        is_cliched = any(re.search(p, old_intro, re.IGNORECASE) for p in cliched_patterns)
        
        # 检查是否已经优化过（过长或包含特殊标记）
        already_optimized = len(old_intro) > 200 or '这座城市' in old_intro or '在' + city in old_intro[:50]
        
        if is_cliched and not already_optimized and len(old_intro) < 400:
            # 生成新开头
            new_intro = generate_intro(district, city, province)
            
            # 替换
            content = content.replace(old_intro, new_intro, 1)
            
            # 写回
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"Error: {filepath} - {e}")
        return False

def main():
    """主函数"""
    fixed_count = 0
    
    docs_dir = 'docs/cities'
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith('.md') or file == 'index.md':
                continue
            
            filepath = os.path.join(root, file)
            
            # 获取地区信息
            parts = filepath.split(os.sep)
            district = file.replace('宠物火化服务.md', '').replace('.md', '')
            city = parts[-2] if len(parts) >= 2 else ''
            province = parts[-3] if len(parts) >= 3 else ''
            
            if fix_article_intro(filepath, province, city, district):
                fixed_count += 1
                if fixed_count % 100 == 0:
                    print(f"已优化 {fixed_count} 篇...")
    
    print(f"\n完成！共优化 {fixed_count} 篇文章的开头")

if __name__ == '__main__':
    main()
