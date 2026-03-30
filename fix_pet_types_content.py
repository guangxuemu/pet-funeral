#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加宠物类型细分内容
- 猫咪火化服务
- 狗狗火化服务  
- 仓鼠/兔子等小型宠物火化
"""

import os
from pathlib import Path

class PetTypeContentAdder:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
    
    def add_pet_type_section_to_faq(self):
        """在FAQ添加宠物类型细分章节"""
        file_path = self.base_dir / 'docs' / 'faq.md'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已添加
        if "不同宠物的火化服务" in content:
            print("✓ 宠物类型章节已存在，跳过")
            return
        
        # 添加宠物类型细分内容
        pet_type_section = """

## 不同宠物的火化服务

### Q: 猫咪火化服务有什么特点？

百情宠物善终提供专业的**猫咪火化服务**，了解猫咪的特殊需求：

- **温柔接宠**：猫咪性格敏感，我们采用温和方式接运
- **单独火化**：确保您的猫咪得到单独的火化服务
- **毛发留存**：可选择留存猫咪毛发制作纪念品
- **骨灰盒选择**：提供适合猫咪体型的精美骨灰盒

猫咪火化费用根据体型而定，一般在几百元到千元左右。

### Q: 狗狗火化服务包含什么？

我们的**狗狗火化服务**覆盖各种犬种：

- **大型犬火化**：配备专业设备，可处理大型犬
- **中型犬火化**：标准火化流程，安全卫生
- **小型犬火化**：精细操作，尊重每一个生命
- **上门接送**：减少狗狗搬运带来的应激

狗狗火化费用：
- 小型犬（10kg以下）：几百元起
- 中型犬（10-25kg）：千元左右
- 大型犬（25kg以上）：千元以上

### Q: 仓鼠、兔子等小型宠物可以火化吗？

可以的。百情宠物善终提供**小型宠物火化服务**：

**可火化的小型宠物包括**：
- 仓鼠、龙猫、豚鼠
- 兔子、蜜袋鼯
- 鸟类（鹦鹉、鸽子等）
- 爬行类（龟、蜥蜴等）

**服务特点**：
- 精细火化，尊重小生命
- 可选择集体火化（费用更低）或单独火化
- 提供小型骨灰盒和纪念品
- 费用一般在几百元以内

### Q: 异宠（爬宠、鸟类）火化有什么注意事项？

**爬宠火化**：
- 乌龟、蜥蜴等可正常火化
- 保留龟壳等特殊需求可提前沟通

**鸟类火化**：
- 提供羽毛留存服务
- 可选择制作羽毛纪念品

请咨询我们的客服，了解具体的异宠火化服务详情。

"""
        
        # 在文件末尾添加
        content = content.rstrip() + pet_type_section
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加宠物类型细分内容: {file_path}")
    
    def add_pet_type_keywords_to_services(self):
        """在服务页面添加宠物类型关键词"""
        file_path = self.base_dir / 'docs' / 'services.md'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已添加
        if "猫咪火化" in content and "狗狗火化" in content:
            print("✓ 服务页宠物类型关键词已存在，跳过")
            return
        
        # 添加宠物类型服务内容
        pet_service_section = """

### 宠物类型细分服务

百情宠物善终提供各类宠物的专业火化服务：

**猫咪火化服务**：
- 温柔接宠，减少应激
- 单独火化，尊重隐私
- 毛发留存，制作纪念品

**狗狗火化服务**：
- 覆盖大中小型犬种
- 专业设备，安全卫生
- 上门接送，省心安心

**小型宠物火化**：
- 仓鼠、兔子、龙猫等
- 鸟类、爬行类宠物
- 精细操作，尊重生命

无论您的爱宠是猫咪、狗狗，还是仓鼠、兔子，我们都将以专业和尊重，为它送上最后的温暖。

"""
        
        # 找到合适的位置插入（在"## 宠物火化服务"之后）
        if "## 宠物火化服务" in content:
            content = content.replace(
                "## 宠物火化服务",
                "## 宠物火化服务\n" + pet_service_section
            )
        else:
            # 添加到文件末尾
            content = content.rstrip() + "\n" + pet_service_section
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加宠物类型关键词: {file_path}")
    
    def add_pet_type_keywords_to_homepage(self):
        """在首页添加宠物类型关键词"""
        file_path = self.base_dir / 'docs' / 'index.md'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已添加
        if "猫咪火化" in content:
            print("✓ 首页宠物类型关键词已存在，跳过")
            return
        
        # 在features部分添加宠物类型
        if "## 我们的服务" in content:
            # 在feature卡片中添加宠物类型
            old_feature = """### 宠物火化

提供单独火化和集体火化服务，设备符合国家标准，卫生安全。"""
            
            new_feature = """### 宠物火化

提供**猫咪火化**、**狗狗火化**及各类小型宠物火化服务。单独火化和集体火化可选，设备符合国家标准，卫生安全。"""
            
            content = content.replace(old_feature, new_feature)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新首页宠物类型关键词: {file_path}")
    
    def run_all(self):
        """执行所有添加"""
        print("开始添加宠物类型细分内容...\n")
        
        print("[1/3] 添加FAQ宠物类型章节...")
        self.add_pet_type_section_to_faq()
        
        print("[2/3] 添加服务页宠物类型内容...")
        self.add_pet_type_keywords_to_services()
        
        print("[3/3] 添加首页宠物类型关键词...")
        self.add_pet_type_keywords_to_homepage()
        
        print("\n✅ 宠物类型细分内容添加完成！")

if __name__ == "__main__":
    adder = PetTypeContentAdder('/home/mz/.openclaw/workspace/pet-funeral')
    adder.run_all()
