<template>
  <div class="contact-card">
    <div class="contact-header">📞 联系我们</div>
    <div class="contact-body">
      <div class="wechat-info">
        <span class="label">微信：</span>
        <span class="value">{{ wechatId }}</span>
        <button class="copy-btn" @click="copyWechat">📋 复制</button>
      </div>
      <p class="tip">点击复制微信号，打开微信搜索添加</p>
      <p v-if="copied" class="copied-tip">✅ 已复制！</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  wechatId: {
    type: String,
    default: '923160208'
  }
})

const copied = ref(false)

const copyWechat = async () => {
  try {
    // 方法1: 使用Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(props.wechatId)
    } else {
      // 方法2: 使用传统方法兼容
      const textArea = document.createElement('textarea')
      textArea.value = props.wechatId
      textArea.style.position = 'fixed'
      textArea.style.left = '-9999px'
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
    }
    
    // 显示复制成功提示
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    // 如果都失败，提示用户手动复制
    alert('请手动复制微信号：' + props.wechatId)
  }
}
</script>

<style scoped>
.contact-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.contact-header {
  background: linear-gradient(135deg, #07C160, #06AD56);
  color: white;
  padding: 12px 16px;
  font-weight: bold;
  font-size: 16px;
}
.contact-body {
  padding: 16px;
  background: #fff;
  position: relative;
}
.wechat-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  flex-wrap: wrap;
}
.label {
  color: #666;
}
.value {
  font-weight: bold;
  color: #07C160;
  font-family: monospace;
}
.copy-btn {
  background: #07C160;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}
.copy-btn:hover {
  background: #06AD56;
  transform: scale(1.05);
}
.copy-btn:active {
  transform: scale(0.95);
}
.tip {
  font-size: 13px;
  color: #999;
  margin-top: 10px;
  margin-bottom: 0;
}
.copied-tip {
  font-size: 14px;
  color: #07C160;
  margin-top: 10px;
  margin-bottom: 0;
  font-weight: bold;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 暗黑模式适配 */
.dark .contact-card {
  border-color: #333;
}
.dark .contact-body {
  background: #1a1a1a;
}
.dark .label {
  color: #aaa;
}
</style>