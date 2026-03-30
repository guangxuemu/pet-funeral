#!/usr/bin/env python3
"""
修复重复的文章开头，确保每个都独一无二
使用更精细的模板 + 地区特色信息
"""

import os
import re
import hashlib

# 为每个地区生成独特开头
def generate_unique_intro(district, city, province):
    """根据地区信息生成独特开头"""
    
    # 使用地区名称生成唯一索引
    unique_key = f"{province}{city}{district}"
    hash_val = int(hashlib.md5(unique_key.encode()).hexdigest(), 16)
    
    # 地区特色描述库
    region_features = {
        '北京': ['胡同', '故宫', '老北京', '首都', '皇城根'],
        '上海': ['外滩', '弄堂', '魔都', '黄浦江', '海派'],
        '广东': ['岭南', '粤语', '珠江', '潮汕', '早茶'],
        '福建': ['闽南', '土楼', '鼓浪屿', '武夷山', '茶香'],
        '浙江': ['西湖', '江南', '乌镇', '钱塘江', '丝绸'],
        '江苏': ['园林', '秦淮河', '姑苏', '太湖', '吴侬软语'],
        '四川': ['宽窄巷子', '火锅', '天府', '锦里', '巴蜀'],
        '山东': ['泰山', '孔孟', '泉城', '青岛', '鲁菜'],
        '河南': ['中原', '黄河', '龙门石窟', '少林', '古都'],
        '河北': ['燕赵', '承德', '山海关', '白洋淀', '燕赵大地'],
        '湖南': ['湘江', '橘子洲', '张家界', '凤凰', '楚湘'],
        '湖北': ['长江', '黄鹤楼', '武当', '三峡', '荆楚'],
        '辽宁': ['沈阳故宫', '大连海滨', '东北', '辽东', '白山黑水'],
        '吉林': ['长白山', '雾凇', '松花江', '东北', '白山松水'],
        '黑龙江': ['哈尔滨', '冰雪', '松花江', '东北', '黑土地'],
        '陕西': ['长安', '兵马俑', '秦岭', '古城', '三秦'],
        '山西': ['晋商', '平遥', '五台山', '黄河', '三晋'],
        '安徽': ['黄山', '徽派', '巢湖', '江淮', '皖南'],
        '江西': ['庐山', '滕王阁', '赣江', '红色', '赣鄱'],
        '云南': ['丽江', '大理', '滇池', '彩云之南', '民族'],
        '贵州': ['黄果树', '遵义', '黔东南', '山地', '黔贵'],
        '广西': ['桂林', '阳朔', '漓江', '壮乡', '八桂'],
        '海南': ['三亚', '椰林', '天涯海角', '热带', '琼州'],
        '内蒙古': ['草原', '呼伦贝尔', '蒙古包', '辽阔', '塞北'],
        '新疆': ['天山', '喀纳斯', '葡萄沟', '西域', '边疆'],
        '西藏': ['拉萨', '布达拉宫', '雪山', '高原', '雪域'],
        '甘肃': ['敦煌', '丝绸之路', '黄河', '西北', '陇原'],
        '青海': ['青海湖', '塔尔寺', '三江源', '高原', '青藏'],
        '宁夏': ['西夏', '贺兰山', '黄河', '塞上', '回乡'],
        '天津': ['津门', '五大道', '海河', '津沽', '渤海'],
        '重庆': ['山城', '洪崖洞', '长江', '火锅', '巴渝'],
        '上海': ['外滩', '弄堂', '黄浦江', '东方明珠', '申城'],
        '海南': ['三亚', '椰林', '天涯海角', '热带', '琼州'],
    }
    
    # 获取城市特色
    city_feature = region_features.get(city, [city, '这座城', '这里', '此地'])
    feature = city_feature[hash_val % len(city_feature)]
    
    # 季节和天气
    seasons = ['春天', '夏天', '秋天', '冬天', '清晨', '黄昏', '夜晚']
    weathers = ['阳光正好', '微风轻拂', '细雨绵绵', '落叶飘零', '雪花飘落', '暮色四合']
    season = seasons[hash_val % len(seasons)]
    weather = weathers[hash_val % len(weathers)]
    
    # 宠物行为描述
    actions = [
        '摇着尾巴迎接你回家',
        '在窗台上晒太阳',
        '蜷缩在你的脚边',
        '在房间里欢快奔跑',
        '用头蹭你的手',
        '静静地看着你',
        '在门口等你下班',
        '陪你一起看电视',
    ]
    action = actions[hash_val % len(actions)]
    
    # 情感描述
    emotions = [
        '那份温暖至今想起仍让人心头一热',
        '那些日子成为记忆中最柔软的部分',
        '这份陪伴早已成为生命中不可或缺的存在',
        '它用无言的爱填满了日常的每个角落',
        '那份忠诚与依赖让人至今难忘',
    ]
    emotion = emotions[hash_val % len(emotions)]
    
    # 场景描述
    scenes = [
        f'{city}{district}的街头巷尾',
        f'{district}的小区花园',
        f'{city}的公园长椅旁',
        f'{district}的家中角落',
        f'{city}的梧桐树下',
        f'{district}的阳台',
        f'{city}{district}的老街',
        f'{district}的林荫道',
    ]
    scene = scenes[hash_val % len(scenes)]
    
    # 构建独特开头（多种句式组合）
    templates = [
        f"{city}的{season}，{weather}。在{scene}，那个曾{action}的小家伙，用一生的陪伴温暖了主人的岁月。{emotion}。如今它离去，在{district}，越来越多的主人开始思考：如何让这份陪伴有一个体面的句点？",
        
        f"{feature}的{city}，{season}的{scene}格外宁静。那个曾{action}的小生命，曾给主人带来无数欢笑。{emotion}。当离别来临，{district}的饲主们开始寻找一种更有温度的方式，送别这位特殊的家人。",
        
        f"{emotion}。在{city}{district}，那个曾{action}的小家伙，用{['数年', '十几年', '无数个日夜'][hash_val % 3]}的陪伴，为主人编织了太多温暖的回忆。{city}的{season}，{weather}，如何好好告别，成为{district}人心中共同的牵挂。",
        
        f"{scene}的{season}，{weather}。主人总会想起那个{action}的小身影。{emotion}。在{district}，为离世的爱宠安排一场温暖的告别，不仅是对它的尊重，更是对这段{['珍贵', '难忘', '美好'][hash_val % 3]}缘分的珍藏。",
        
        f"有人说，宠物的生命虽然短暂，却足以温暖一生。在{city}{district}，那个曾{action}的小家伙，走到了生命的终点。{emotion}。{city}的{feature}旁，主人开始寻求一种更体面的方式，送它最后一程。",
        
        f"{city}的{feature}，见证了无数人与宠物的故事。在{district}，那个曾{action}的小生命，用{['忠诚', '温柔', '活泼'][hash_val % 3]}的陪伴，成为家庭中不可或缺的一员。{season}，{weather}，{emotion}，如何好好告别，是每位饲主心中的牵挂。",
        
        f"{scene}，{weather}。那个曾{action}的小家伙，留下了太多温暖的回忆。{emotion}。在{city}{district}，越来越多的主人意识到：为离世的爱宠安排一场有尊严的告别，是对这份陪伴最好的回应。",
        
        f"{city}的{season}总是格外{['温柔', '宁静', '美好'][hash_val % 3]}。在{district}，那个曾{action}的小生命，走到了旅程的终点。{emotion}。{feature}的{city}，开始用更温暖的方式，守护每一份离别。",
    ]
    
    # 根据hash选择模板
    selected_template = templates[hash_val % len(templates)]
    
    return selected_template

def fix_duplicate_intros():
    """修复重复开头"""
    
    # 收集所有已优化的开头
    intros_seen = {}
    duplicates = []
    
    docs_dir = 'docs/cities'
    
    # 第一遍：收集所有开头
    print("第一遍：收集所有开头...")
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith('.md') or file == 'index.md':
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取开头
                patterns = [
                    r'<DistrictList />\n\n\n+(.*?)\n\n---',
                    r'<DistrictList />\n\n\n+(.*?)\n##',
                    r'<Breadcrumb />\n\n<DistrictList />\n\n\n+(.*?)\n\n---',
                ]
                
                intro = None
                for pattern in patterns:
                    match = re.search(pattern, content, re.DOTALL)
                    if match:
                        intro = match.group(1).strip()
                        break
                
                if intro:
                    # 检查是否重复
                    intro_key = intro[:50]  # 取前50字符作为key
                    if intro_key in intros_seen:
                        duplicates.append(filepath)
                    else:
                        intros_seen[intro_key] = filepath
                        
            except:
                pass
    
    print(f"发现 {len(duplicates)} 篇重复开头")
    
    # 第二遍：修复重复
    print("\n第二遍：修复重复开头...")
    fixed_count = 0
    
    for filepath in duplicates:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取地区信息
            parts = filepath.split(os.sep)
            district = parts[-1].replace('宠物火化服务.md', '').replace('.md', '')
            city = parts[-2] if len(parts) >= 2 else ''
            province = parts[-3] if len(parts) >= 3 else ''
            
            # 提取旧开头
            old_intro = None
            for pattern in patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    old_intro = match.group(1).strip()
                    break
            
            if old_intro:
                # 生成新开头
                new_intro = generate_unique_intro(district, city, province)
                
                # 替换
                content = content.replace(old_intro, new_intro, 1)
                
                # 写回
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                if fixed_count % 50 == 0:
                    print(f"已修复 {fixed_count} 篇...")
                    
        except Exception as e:
            print(f"Error: {filepath} - {e}")
    
    print(f"\n完成！共修复 {fixed_count} 篇重复开头")

if __name__ == '__main__':
    fix_duplicate_intros()
