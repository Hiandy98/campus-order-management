<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type Stock } from '../api'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
import { RouterLink } from 'vue-router'

const STORAGE_KEY = 'pos_custom_order'

const localStocks = ref<Stock[]>([])
const isLoading = ref(true)
const isSaving = ref(false)
const saveSuccess = ref(false)

onMounted(async () => {
  try {
    const data = await api.getStocks()
    const savedOrder = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') as string[]

    data.sort((a, b) => {
      const indexA = savedOrder.indexOf(a.name)
      const indexB = savedOrder.indexOf(b.name)
      return (indexA === -1 ? 999 : indexA) - (indexB === -1 ? 999 : indexB)
    })
    
    localStocks.value = data
  } catch (e) {
    alert('載入失敗')
  } finally {
    isLoading.value = false
  }
})

const moveUp = (index: number) => {
  if (index === 0) return
  const temp = localStocks.value[index]
  localStocks.value[index] = localStocks.value[index - 1]
  localStocks.value[index - 1] = temp
}

const moveDown = (index: number) => {
  if (index === localStocks.value.length - 1) return
  const temp = localStocks.value[index]
  localStocks.value[index] = localStocks.value[index + 1]
  localStocks.value[index + 1] = temp
}

const saveOrder = () => {
  isSaving.value = true
  const names = localStocks.value.map((item) => item.name)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(names))
  
  setTimeout(() => {
    isSaving.value = false
    saveSuccess.value = true
    setTimeout(() => (saveSuccess.value = false), 2000)
  }, 300)
}
</script>

<template>
  <PageLayout>
    <PageHeader eyebrow="Admin" title="自訂商品排序">
      <template #action>
        <RouterLink to="/" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
          ← 返回點餐
        </RouterLink>
      </template>
    </PageHeader>

    <main class="mt-8 flex-1">
      <p v-if="isLoading" class="text-ink-mute animate-pulse">載入商品中...</p>
      
      <div v-else class="flex flex-col gap-3">
        <div 
          v-for="(item, index) in localStocks" 
          :key="item.name"
          class="flex items-center justify-between rounded-xl border border-line bg-surface p-4"
        >
          <span class="text-lg font-bold text-ink">{{ item.name }}</span>
          
          <div class="flex gap-2">
            <button 
              @click="moveUp(index)" 
              :disabled="index === 0"
              class="flex h-10 w-10 items-center justify-center rounded-lg border border-line bg-paper text-ink-mute hover:text-ink disabled:opacity-30 disabled:cursor-not-allowed active:scale-95"
            >
              ↑
            </button>
            <button 
              @click="moveDown(index)" 
              :disabled="index === localStocks.length - 1"
              class="flex h-10 w-10 items-center justify-center rounded-lg border border-line bg-paper text-ink-mute hover:text-ink disabled:opacity-30 disabled:cursor-not-allowed active:scale-95"
            >
              ↓
            </button>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-line">
          <button 
            @click="saveOrder"
            :disabled="isSaving"
            class="w-full rounded-xl bg-ink py-4 text-lg font-bold text-paper transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-50"
            :class="saveSuccess ? 'bg-green-600' : 'bg-ink'"
          >
            {{ isSaving ? '儲存中...' : saveSuccess ? '✓ 儲存成功' : '儲存排序' }}
          </button>
        </div>
      </div>
    </main>
  </PageLayout>
</template>