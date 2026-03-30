<template>
  <nav class="breadcrumb" aria-label="面包屑导航">
    <ol class="breadcrumb-list" itemscope itemtype="https://schema.org/BreadcrumbList">
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a href="/" itemprop="item">
          <span itemprop="name">首页</span>
        </a>
        <meta itemprop="position" content="1" />
      </li>
      <li v-for="(item, index) in items" :key="index" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span class="separator">/</span>
        <a v-if="item.link" :href="item.link" itemprop="item">
          <span itemprop="name">{{ item.text }}</span>
        </a>
        <span v-else itemprop="name">{{ item.text }}</span>
        <meta itemprop="position" :content="index + 2" />
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'

const { page } = useData()

const items = computed(() => {
  const path = page.value.relativePath
  // 过滤掉空字符串和index.md
  const parts = path.split('/').filter(p => p && p !== 'index.md')
  
  // 城市页面面包屑
  if (parts[0] === 'cities') {
    const regionMap = {
      'huadong': '华东地区',
      'huabei': '华北地区',
      'huazhong': '华中地区',
      'huanan': '华南地区',
      'xinan': '西南地区',
      'xibei': '西北地区',
      'dongbei': '东北地区'
    }
    
    const result = [{ text: '城市服务', link: '/cities/' }]
    
    if (parts.length >= 2) {
      const region = parts[1]
      result.push({ text: regionMap[region] || region, link: `/cities/${region}/` })
    }
    
    if (parts.length >= 3) {
      result.push({ text: parts[2], link: `/cities/${parts[1]}/${parts[2]}/` })
    }
    
    if (parts.length >= 4) {
      // 区县页面，去掉.md后缀和"宠物火化服务"后缀
      const district = parts[3].replace('.md', '').replace('宠物火化服务', '')
      result.push({ text: district })
    }
    
    return result
  }
  
  // 其他页面
  const pageMap = {
    'services': '服务介绍',
    'faq': '常见问题',
    'about': '关于我们',
    'memorial': '纪念品'
  }
  
  const pageName = parts[0]?.replace('.md', '')
  if (pageMap[pageName]) {
    return [{ text: pageMap[pageName] }]
  }
  
  return []
})
</script>

<style scoped>
.breadcrumb {
  padding: 12px 0;
  font-size: 14px;
  color: #666;
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 4px;
}

.breadcrumb-list li {
  display: flex;
  align-items: center;
}

.breadcrumb-list a {
  color: #3b82f6;
  text-decoration: none;
}

.breadcrumb-list a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 4px;
  color: #999;
}

/* 暗黑模式 */
.dark .breadcrumb {
  color: #aaa;
}

.dark .breadcrumb-list a {
  color: #60a5fa;
}
</style>