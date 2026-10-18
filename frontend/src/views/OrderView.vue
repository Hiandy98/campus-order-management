<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api'

const msg = ref('載入中…')

onMounted(async () => {
  try {
    const stocks = await api.getStocks()
    msg.value = `後端連線 OK，庫存 ${stocks.length} 筆`
  } catch (e: any) {
    msg.value = `${e.message}`
  }
})
</script>

<template>
  <div class="py-20 text-center text-lg text-gray-500">{{ msg }}</div>
</template>