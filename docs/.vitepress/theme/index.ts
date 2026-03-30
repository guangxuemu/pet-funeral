import DefaultTheme from 'vitepress/theme'
import MyContact from './MyContact.vue'
import Breadcrumb from './Breadcrumb.vue'
import DistrictList from './DistrictList.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 注册全局组件
    app.component('MyContact', MyContact)
    app.component('Breadcrumb', Breadcrumb)
    app.component('DistrictList', DistrictList)
  }
}
