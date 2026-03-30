import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '宠物殡葬善终',
  description: '专业宠物殡葬火化服务平台，提供全国上门接送、单独火化、告别仪式、骨灰纪念等一站式服务。',
  lang: 'zh-CN',
  
  vite: {
    server: {
      port: 5000,
      host: '0.0.0.0',
      allowedHosts: ['test.quanwushan.com', '.quanwushan.com']
    }
  },
  
  head: [
    ['meta', { name: 'keywords', content: '宠物殡葬,宠物火化,宠物安葬,宠物告别,宠物纪念品,宠物骨灰' }],
    ['meta', { name: 'author', content: '宠物殡葬善终' }],
    ['meta', { name: 'robots', content: 'index, follow' }],
    ['meta', { name: 'googlebot', content: 'index, follow' }],
    ['meta', { name: 'baiduspider', content: 'index, follow' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: '宠物殡葬善终' }],
    ['meta', { property: 'og:locale', content: 'zh_CN' }],
    ['meta', { property: 'og:image', content: 'https://www.cwbzxxw.com/logo.png' }],
    ['meta', { name: 'format-detection', content: 'telephone=no' }],
    ['link', { rel: 'canonical', href: 'https://www.cwbzxxw.com/' }],
  ],
  
  themeConfig: {
    logo: '/logo.png',
    siteTitle: '宠物殡葬善终',
    
    nav: [
      { text: '首页', link: '/' },
      { text: '服务介绍', link: '/services' },
      { text: '城市服务', link: '/cities/' },
      { text: '纪念品', link: '/memorial' },
      { text: '常见问题', link: '/faq' },
      { text: '关于我们', link: '/about' },
    ],
    
    sidebar: {
      '/cities/': [
        {
          text: '城市服务导航',
          items: [
            { text: '全国城市', link: '/cities/' }
          ]
        },
        {
          text: '华东地区',
          collapsed: true,
          items: [
            { text: '上海', link: '/cities/上海/' },
            { text: '江苏', link: '/cities/江苏/' },
            { text: '浙江', link: '/cities/浙江/' },
            { text: '安徽', link: '/cities/安徽/' },
            { text: '福建', link: '/cities/福建/' },
            { text: '江西', link: '/cities/江西/' },
            { text: '山东', link: '/cities/山东/' },
          ]
        },
        {
          text: '华北地区',
          collapsed: true,
          items: [
            { text: '北京', link: '/cities/北京/' },
            { text: '天津', link: '/cities/天津/' },
            { text: '河北', link: '/cities/河北/' },
            { text: '山西', link: '/cities/山西/' },
            { text: '内蒙古', link: '/cities/内蒙古/' },
          ]
        },
        {
          text: '华南地区',
          collapsed: true,
          items: [
            { text: '广东', link: '/cities/广东/' },
            { text: '广西', link: '/cities/广西/' },
            { text: '海南', link: '/cities/海南/' },
          ]
        },
        {
          text: '华中地区',
          collapsed: true,
          items: [
            { text: '河南', link: '/cities/河南/' },
            { text: '湖北', link: '/cities/湖北/' },
            { text: '湖南', link: '/cities/湖南/' },
          ]
        },
        {
          text: '东北地区',
          collapsed: true,
          items: [
            { text: '辽宁', link: '/cities/辽宁/' },
            { text: '吉林', link: '/cities/吉林/' },
            { text: '黑龙江', link: '/cities/黑龙江/' },
          ]
        },
        {
          text: '西南地区',
          collapsed: true,
          items: [
            { text: '重庆', link: '/cities/重庆/' },
            { text: '四川', link: '/cities/四川/' },
            { text: '贵州', link: '/cities/贵州/' },
            { text: '云南', link: '/cities/云南/' },
            { text: '西藏', link: '/cities/西藏/' },
          ]
        },
        {
          text: '西北地区',
          collapsed: true,
          items: [
            { text: '陕西', link: '/cities/陕西/' },
            { text: '甘肃', link: '/cities/甘肃/' },
            { text: '青海', link: '/cities/青海/' },
            { text: '宁夏', link: '/cities/宁夏/' },
            { text: '新疆', link: '/cities/新疆/' },
          ]
        },
      ]
    },
    
    footer: {
      message: '专业宠物殡葬善终 | 微信: 923160208',
      copyright: 'Copyright © 2026 百情宠物善终'
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
    hostname: 'https://www.cwbzxxw.com'
  },
  
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true
})
