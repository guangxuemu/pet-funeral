#!/bin/bash
echo "========== 百情宠物善终 全面站点检查 =========="
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

echo "## 1. 文件统计"
echo "---"
echo "总Markdown文件数: $(find docs -name '*.md' | wc -l)"
echo "省份页面: $(find docs/cities -maxdepth 1 -name 'index.md' | wc -l)"
echo "城市页面: $(find docs/cities -mindepth 2 -maxdepth 2 -name 'index.md' | wc -l)"
echo "区县页面: $(find docs/cities -mindepth 3 -name '*.md' | wc -l)"
echo ""

echo "## 2. 重复内容检查"
echo "---"
echo "完全相同的title数量:"
grep -r "^title: " docs/ --include="*.md" | sort | uniq -d | wc -l
echo ""
echo "相似description数量(前100字符相同):"
grep -r "^description: " docs/cities/ --include="*.md" | cut -c1-100 | sort | uniq -d | wc -l
echo ""

echo "## 3. 404链接检查"
echo "---"
echo "潜在404链接统计:"
grep -rE '\[([^\]]+)\]\((/[^)]+)\)' docs/ --include="*.md" | grep -oE '/[^)]+' | sort | uniq -c | sort -rn | head -20
echo ""

echo "## 4. 内部链接完整性"
echo "---"
echo "总内部链接数: $(grep -rE '\[([^\]]+)\]\((/[^)]+)\)' docs/ --include="*.md" | wc -l)"
echo "唯一链接数: $(grep -rE '\[([^\]]+)\]\((/[^)]+)\)' docs/ --include="*.md" | grep -oE '/[^)]+' | sort -u | wc -l)"
echo ""

echo "## 5. 内容遗漏检查"
echo "---"
echo "缺少description的页面:"
find docs -name "*.md" -exec grep -L "^description:" {} \; | wc -l
echo ""
echo "缺少keywords的页面:"
find docs -name "*.md" -exec grep -L "^keywords:" {} \; | wc -l
echo ""

echo "## 6. 多余内容检查"
echo "---"
echo "HTML标签残留:"
grep -r "<[^>]*>" docs/ --include="*.md" | wc -l
echo ""
echo "空行统计(超过3行连续空行):"
grep -n "^$" docs/index.md docs/services.md docs/faq.md docs/about.md 2>/dev/null | head -10
echo ""

echo "## 7. Title/H1一致性抽查"
echo "---"
for city in 北京 上海 广州 深圳 杭州 成都; do
    if [ -f "docs/cities/*/$city/index.md" ]; then
        title=$(grep "^title: " docs/cities/*/$city/index.md 2>/dev/null | head -1 | sed 's/title: //' | cut -d'|' -f1 | tr -d ' ')
        h1=$(grep "^# " docs/cities/*/$city/index.md 2>/dev/null | head -1 | sed 's/# //' | cut -d'：' -f1 | tr -d ' ')
        if [ "$title" = "$h1" ]; then
            echo "✅ $city: 一致"
        else
            echo "⚠️ $city: 不一致"
            echo "   Title: $title"
            echo "   H1: $h1"
        fi
    fi
done
echo ""

echo "## 8. 关键词覆盖检查"
echo "---"
echo "'宠物火化'出现: $(grep -r '宠物火化' docs/ --include='*.md' | wc -l) 次"
echo "'宠物殡葬'出现: $(grep -r '宠物殡葬' docs/ --include='*.md' | wc -l) 次"
echo "'24小时'出现: $(grep -r '24小时' docs/ --include='*.md' | wc -l) 次"
echo "'正规宠物火化机构'出现: $(grep -r '正规宠物火化机构' docs/ --include='*.md' | wc -l) 次"
echo ""

echo "========== 检查完成 =========="
