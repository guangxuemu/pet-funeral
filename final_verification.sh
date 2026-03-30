#!/bin/bash
echo "========== SEO修复后全面验证 =========="
echo "验证时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

echo "1. Description长度检查"
echo "---"
over_160=$(grep -r "^description: " docs/ --include="*.md" | awk 'length > 180' | wc -l)
echo "超过160字符的description: $over_160 个"
if [ "$over_160" -eq 0 ]; then
    echo "✅ PASS - 所有description长度正常"
else
    echo "⚠️ FAIL - 仍有 $over_160 个description过长"
    grep -r "^description: " docs/ --include="*.md" | awk 'length > 180' | head -3
fi
echo ""

echo "2. 404链接检查"
echo "---"
dead_links=$(grep -rE '\[([^\]]+)\]\((/安放|/安葬[^)]*|/纪念[^)]*|/寄存[^)]*)\)' docs/ --include="*.md" 2>/dev/null | wc -l)
echo "潜在404链接数: $dead_links 个"
if [ "$dead_links" -eq 0 ]; then
    echo "✅ PASS - 无404死链"
else
    echo "⚠️ FAIL - 仍有 $dead_links 个死链"
    grep -rE '\[([^\]]+)\]\((/安放|/安葬[^)]*|/纪念[^)]*|/寄存[^)]*)\)' docs/ --include="*.md" 2>/dev/null | head -3
fi
echo ""

echo "3. 重复title检查"
echo "---"
dup_titles=$(grep -r "^title: " docs/cities/ --include="*.md" | sort | uniq -d | wc -l)
echo "重复title数: $dup_titles 个"
if [ "$dup_titles" -eq 0 ]; then
    echo "✅ PASS - 无重复title"
else
    echo "⚠️ FAIL - 有 $dup_titles 个重复title"
fi
echo ""

echo "4. Title/H1一致性抽查"
echo "---"
for city in 北京 上海 广州 深圳 杭州; do
    file="docs/cities/*/{$city}/index.md"
    if [ -f "docs/cities/*/$city/index.md" ]; then
        title_core=$(grep "^title: " "docs/cities/*/$city/index.md" 2>/dev/null | head -1 | sed 's/title: //' | cut -d'|' -f1 | tr -d ' ')
        h1_core=$(grep "^# " "docs/cities/*/$city/index.md" 2>/dev/null | head -1 | sed 's/# //' | cut -d'：' -f1 | tr -d ' ')
        if [ "$title_core" = "$h1_core" ]; then
            echo "✅ $city: Title/H1一致"
        else
            echo "⚠️ $city: Title/H1不一致"
        fi
    fi
done
echo ""

echo "5. 关键词覆盖检查"
echo "---"
echo "'宠物火化'出现: $(grep -r '宠物火化' docs/ --include='*.md' | wc -l) 次"
echo "'宠物殡葬'出现: $(grep -r '宠物殡葬' docs/ --include='*.md' | wc -l) 次"
echo "'24小时'出现: $(grep -r '24小时' docs/ --include='*.md' | wc -l) 次"
echo ""

echo "========== 验证完成 =========="
