<template>
  <Layout>
    <!-- JSON-LD 结构化数据 -->
    <Head>
      <script type="application/ld+json" v-html="structuredData"></script>
    </Head>
  </Layout>
</template>

<script setup>
import { computed } from 'vue'
import { useData, Head } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

const { frontmatter, page } = useData()
const Layout = DefaultTheme.Layout

// 结构化数据
const structuredData = computed(() => {
  const baseData = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "百情宠物善终",
    "description": "专业宠物殡葬服务，提供宠物火化、告别仪式、骨灰纪念等一站式服务",
    "url": "https://www.petfuneral.cn",
    "telephone": "400-XXX-XXXX",
    "areaServed": {
      "@type": "Country",
      "name": "中国"
    },
    "serviceType": ["宠物火化", "宠物殡葬", "宠物告别", "骨灰纪念"],
    "priceRange": "￥￥",
    "openingHours": "Mo-Su 00:00-23:59",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "80000"
    }
  }

  // 城市页面添加本地业务信息
  if (frontmatter.value.keywords) {
    const keywords = frontmatter.value.keywords
    if (keywords.some(k => k.includes('宠物火化'))) {
      return {
        ...baseData,
        "name": `百情宠物善终 - ${keywords[0].replace('宠物火化', '')}`,
        "serviceType": keywords
      }
    }
  }

  return baseData
})
</script>