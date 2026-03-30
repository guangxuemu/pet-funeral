#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物殡葬文章配图生成器
使用 Stable Horde API 生成温馨的宠物纪念图片
"""

import subprocess
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Stable Horde API 配置
STABLE_HORDE_API_KEY = "kZxgQ09h2TzJendjn_oFYQ"
STABLE_HORDE_API = "https://aihorde.net/api/v2"

# 图片生成脚本路径
IMAGE_SCRIPT = Path("/home/.openclaw/workspace/skills/skills/stable-horde-generator/generate.sh")

# 图片输出目录
IMAGE_OUTPUT_DIR = Path("/home/.openclaw/workspace/pet-funeral/docs/images")

# 图片提示词模板
IMAGE_PROMPTS = {
    "memorial": {
        "prompt": "heartwarming pet memorial scene, beloved dog or cat peacefully resting on soft blanket surrounded by white flowers and glowing candles, warm golden sunlight, peaceful atmosphere, no coffin, touching and beautiful, photorealistic, 8k quality",
        "model": "AbsoluteReality",
        "desc": "温馨纪念场景"
    },
    "farewell": {
        "prompt": "pet farewell ceremony, gentle hands holding a small pet, warm indoor lighting, flowers and candles, peaceful and dignified atmosphere, professional pet cremation service, no coffin, emotional and touching, photorealistic",
        "model": "Realistic Vision", 
        "desc": "告别仪式场景"
    },
    "rainbow_bridge": {
        "prompt": "rainbow bridge pet farewell, beloved pet walking towards beautiful rainbow in golden sunset sky, looking back with peaceful smile, fluffy white clouds, heavenly light rays, no coffin, touching emotional moment, fantasy ethereal art style, dreamlike and beautiful, 4k detailed",
        "model": "Dreamshaper",
        "desc": "彩虹桥告别"
    },
    "service": {
        "prompt": "professional pet cremation service center, clean and dignified interior, soft lighting, flowers arrangement, peaceful atmosphere, respectful environment, modern facility, no coffin, photorealistic, 8k",
        "model": "Deliberate",
        "desc": "服务中心环境"
    },
    "comfort": {
        "prompt": "comforting scene, person hugging their beloved pet dog or cat, warm embrace, soft natural lighting, emotional and touching moment, love and companionship, photorealistic, heartwarming",
        "model": "AbsoluteReality",
        "desc": "温馨陪伴场景"
    }
}


def generate_image(prompt: str, model: str, output_path: Path, width: int = 768, height: int = 512) -> Tuple[bool, str]:
    """
    使用 Stable Horde 生成图片
    
    Args:
        prompt: 图片描述
        model: 模型名称
        output_path: 输出路径
        width: 图片宽度
        height: 图片高度
    
    Returns:
        (success, message)
    """
    if not IMAGE_SCRIPT.exists():
        return False, f"图片生成脚本不存在: {IMAGE_SCRIPT}"
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 调用生成脚本
        result = subprocess.run(
            [
                str(IMAGE_SCRIPT),
                prompt,
                "--model", model,
                "--width", str(width),
                "--height", str(height)
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            cwd=IMAGE_SCRIPT.parent
        )
        
        if result.returncode == 0:
            # 解析输出，找到生成的图片路径
            output = result.stdout
            # 提取图片路径
            match = re.search(r'"local_path":\s*"([^"]+)"', output)
            if match:
                generated_path = Path(match.group(1))
                if generated_path.exists():
                    # 移动到目标位置
                    generated_path.rename(output_path)
                    return True, str(output_path)
            
            return False, "无法解析生成的图片路径"
        else:
            return False, f"生成失败: {result.stderr[:200]}"
            
    except subprocess.TimeoutExpired:
        return False, "生成超时"
    except Exception as e:
        return False, f"生成异常: {e}"


def generate_article_images(province: str, city: str, district: str, article_id: str) -> Dict[str, str]:
    """
    为文章生成配图（每篇文章只生成1张）
    
    Args:
        province: 省份
        city: 城市
        district: 区县
        article_id: 文章ID（用于命名图片）
    
    Returns:
        图片类型到路径的映射
    """
    images = {}
    
    # 创建图片目录
    image_dir = IMAGE_OUTPUT_DIR / article_id
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # 每篇文章只生成1张：温馨纪念场景
    img_type = "memorial"
    config = IMAGE_PROMPTS[img_type]
    output_path = image_dir / f"{img_type}.webp"
    
    # 如果图片已存在，跳过
    if output_path.exists():
        images[img_type] = str(output_path.relative_to(IMAGE_OUTPUT_DIR.parent))
        print(f"  ⏭️  配图已存在，跳过")
        return images
    
    print(f"  📸 生成配图: {config['desc']}...")
    
    success, msg = generate_image(
        prompt=config["prompt"],
        model=config["model"],
        output_path=output_path
    )
    
    if success:
        images[img_type] = str(output_path.relative_to(IMAGE_OUTPUT_DIR.parent))
        print(f"  ✅ 配图完成")
    else:
        print(f"  ❌ 配图失败: {msg}")
    
    return images


def insert_images_into_content(content: str, images: Dict[str, str], article_id: str) -> str:
    """
    在文章内容中插入图片（插入到开头段落之后、服务流程之前）
    
    Args:
        content: 原始文章内容
        images: 图片映射 {类型: 路径}
        article_id: 文章ID
    
    Returns:
        插入图片后的内容
    """
    if not images:
        return content
    
    lines = content.split('\n')
    new_lines = []
    
    # 获取第一张图片
    img_path = list(images.values())[0]
    
    # 在"服务流程"标题之前插入图片
    inserted = False
    for i, line in enumerate(lines):
        # 找到"服务流程"标题，在它之前插入图片
        if ('服务流程' in line or '### 服务' in line) and not inserted:
            new_lines.append('')
            new_lines.append(f'![温馨纪念场景]({img_path})')
            new_lines.append('')
            inserted = True
        
        new_lines.append(line)
    
    # 如果没找到服务流程，就在第二个 ### 之前插入
    if not inserted:
        new_lines = []
        heading_count = 0
        for line in lines:
            new_lines.append(line)
            if line.startswith('###'):
                heading_count += 1
                if heading_count == 1 and not inserted:
                    new_lines.append('')
                    new_lines.append(f'![温馨纪念场景]({img_path})')
                    new_lines.append('')
                    inserted = True
    
    return '\n'.join(new_lines)


def get_or_generate_images(province: str, city: str, district: str, article_id: str, force: bool = False) -> Dict[str, str]:
    """
    获取或生成文章配图（每篇文章1张）
    
    Args:
        province: 省份
        city: 城市  
        district: 区县
        article_id: 文章ID
        force: 是否强制重新生成
    
    Returns:
        图片映射
    """
    image_dir = IMAGE_OUTPUT_DIR / article_id
    
    # 检查是否已有图片
    if not force and image_dir.exists():
        img_path = image_dir / "memorial.webp"
        if img_path.exists():
            print(f"  📁 使用已有配图")
            return {"memorial": str(img_path.relative_to(IMAGE_OUTPUT_DIR.parent))}
    
    # 生成新图片
    return generate_article_images(province, city, district, article_id)


# 测试
if __name__ == "__main__":
    # 测试图片生成
    print("测试图片生成（每篇文章1张）...")
    
    test_images = generate_article_images("北京", "北京", "", "test_article")
    print(f"\n生成的图片: {test_images}")
    
    # 测试内容插入
    test_content = """# 北京宠物火化服务

<MyContact />

### 开头段落

每个毛孩子都是家人...

### 服务流程

- 预约咨询
- 专车接运

<MyContact />
"""
    
    if test_images:
        new_content = insert_images_into_content(test_content, test_images, "test_article")
        print("\n插入图片后的内容:")
        print(new_content)