#!/bin/bash
# SEO全面检查脚本

echo "========== 百情宠物善终 SEO全面检查报告 =========="
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 统计文件数量
echo "## 1. 站点文件统计"
echo "总Markdown文件数: $(find docs -name '*.md' | wc -l)"
echo "省份页面: $(find docs/cities -maxdepth 1 -name 'index.md' | wc -l)"
echo "城市页面: $(find docs/cities -mindepth 2 -maxdepth 2 -name 'index.md' | wc -l)"
echo "区县页面: $(find docs/cities -mindepth 3 -name '*.md' | wc -l)"
echo ""

# 2. 检查重复title
echo "## 2. 重复Title检查"
echo "完全相同的title数量:"
grep -r "^title: " docs/ --include="*.md" | sort | uniq -d | wc -l
echo ""

# 3. 检查description问题
echo "## 3. Description检查"
echo "description长度超过160字符的页面:"
grep -r "^description: " docs/ --include="*.md" | awk 'length > 180' | wc -l
echo ""

# 4. 检查链接
echo "## 4. 内部链接检查"
echo "总内部链接数: $(grep -rE '\[.*?\]\((/[^)]+)\)' docs/ --include="*.md" | wc -l)"
echo "唯一链接数: $(grep -rE '\[.*?\]\((/[^)]+)\)' docs/ --include="*.md" | grep -oE '/[^)]+' | sort -u | wc -l)"
echo ""

# 5. 检查可能的404链接
echo "## 5. 潜在404检查"
echo "检查链接指向的文件是否存在..."
grep -rE '\[.*?\]\((/[^)]+)\)' docs/ --include="*.md" | grep -oE '/[^)]+' | sort -u | while read link; do
    file_path="docs${link}.md"
    if [ ! -f "$file_path" ] && [ ! -d "docs${link}" ]; then
        echo "潜在404: $link"
    fi
done | head -20
echo ""

# 6. 检查关键词覆盖
echo "## 6. 关键词覆盖检查"
echo "'宠物火化'出现次数: $(grep -r '宠物火化' docs/ --include="*.md" | wc -l)"
echo "'宠物殡葬'出现次数: $(grep -r '宠物殡葬' docs/ --include="*.md" | wc -l)"
echo "'24小时'出现次数: $(grep -r '24小时' docs/ --include="*.md" | wc -l)"
echo ""

# 7. 检查内容重复度
echo "## 7. 内容重复度检查"
echo "检查相似description..."
grep -r "^description: " docs/cities/ --include="*.md" | sort | uniq -d | wc -l
echo ""

echo "========== 检查完成 =========="
