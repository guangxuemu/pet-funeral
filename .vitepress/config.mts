import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '宠物殡葬服务网',
  description: '专业宠物殡葬火化服务平台，提供全国上门接送、单独火化、告别仪式、骨灰纪念等一站式服务。',
  lang: 'zh-CN',
  
  head: [
    ['meta', { name: 'keywords', content: '宠物殡葬,宠物火化,宠物安葬,宠物告别,宠物纪念品,宠物骨灰' }],
    ['meta', { name: 'author', content: '宠物殡葬服务网' }],
    ['meta', { name: 'robots', content: 'index, follow' }],
  ],
  
  themeConfig: {
    logo: '/logo.png',
    siteTitle: '宠物殡葬服务网',
    
    nav: [
      { text: '首页', link: '/' },
      { text: '服务介绍', link: '/services' },
      { text: '城市服务', link: '/cities' },
      { text: '纪念品', link: '/memorial' },
      { text: '常见问题', link: '/faq' },
      { text: '关于我们', link: '/about' },
    ],
    
    socialLinks: [
      { icon: 'phone', link: 'tel:400-XXX-XXXX' },
    ],
    
    footer: {
      message: '专业宠物殡葬服务 | 24小时热线: 400-XXX-XXXX',
      copyright: 'Copyright © 2024 宠物殡葬服务网'
    },
    
    search: {
      provider: 'local'
    },
    
    outline: {
      level: [2, 3],
      label: '目录'
    },
    
    docFooter: {
      prev: '上一页',
      next: '下一页'
    }
  },
  
  sitemap: {
    hostname: 'https://www.petfuneral.cn'
  },
  
  cleanUrls: true,
  lastUpdated: true
})