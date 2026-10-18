<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../api'

const state = ref<'loading' | 'ok' | 'error'>('loading')
const message = ref('')
const count = ref(0)

onMounted(async () => {
  try {
    const stocks = await api.getStocks()
    state.value = 'ok'
    count.value = stocks.length
  } catch (e: any) {
    state.value = 'error'
    message.value = e.message
  }
})
</script>

<template>
  <div class="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-5 pt-8 pb-10">
    
    <header class="flex items-start justify-between">
      <div>
        <p class="eyebrow mb-2">POS System</p>
        <h1 class="text-3xl font-bold tracking-tight text-ink">點餐區</h1>
      </div>
      
      <div class="flex gap-4 pt-1">
        <RouterLink to="/kitchen" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
          查看備餐 ↗
        </RouterLink>
        <RouterLink to="/pickup" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
          查看取餐 ↗
        </RouterLink>
      </div>
    </header>

    <main class="mt-12 flex-1">
      <template v-if="state === 'loading'">
        <p class="text-ink-mute animate-pulse">正在連線系統...</p>
      </template>

      <template v-else-if="state === 'error'">
        <p class="text-sm text-ink-mute mb-1">連線失敗</p>
        <p class="text-lg text-danger">{{ message }}</p>
      </template>

      <template v-else>
        <p class="text-3xl font-semibold tracking-tight tabular">
          庫存 <span class="text-brand">{{ count }}</span> 筆
        </p>
        <p class="mt-2 text-sm text-ink-soft">系統已就緒，請開始點餐。</p>
      </template>
    </main>
    
  </div>
</template>