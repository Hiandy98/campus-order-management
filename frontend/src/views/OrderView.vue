<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type Stock } from '../api'
import { usePolling } from '../usePolling'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'

const stocks = ref<Stock[]>([])
const isLoading = ref(true)
const errorMsg = ref('')

const cart = reactive<Record<string, number>>({})

const cartTotalCount = computed(() => Object.values(cart).reduce((a, b) => a + b, 0))
const cartTotalPrice = computed(() => {
  return Object.entries(cart).reduce((sum, [name, qty]) => {
    const item = stocks.value.find((s) => s.name === name)
    return sum + (item?.price || 0) * qty
  }, 0)
})

const fetchStocks = async () => {
  try {
    stocks.value = await api.getStocks()
    errorMsg.value = ''
  } catch (e: any) {
    errorMsg.value = e.message
  } finally {
    isLoading.value = false
  }
}

usePolling(fetchStocks, 10000)

const addToCart = (item: Stock) => {
  if (item.soldout) return
  const currentQty = cart[item.name] || 0
  if (currentQty >= item.stock) return
  cart[item.name] = currentQty + 1
}

const removeFromCart = (item: Stock) => {
  const currentQty = cart[item.name] || 0
  if (currentQty > 0) {
    cart[item.name] = currentQty - 1
  }
}

const getStockText = (stock: number, soldout: boolean) => {
  if (soldout || stock <= 0) return { text: '已售完', class: 'text-ink-mute' }
  if (stock <= 10) return { text: `僅剩 ${stock}`, class: 'text-red-500 font-medium' }
  if (stock <= 30) return { text: `剩 ${stock}`, class: 'text-amber-500' }
  return { text: '充足', class: 'text-ink-mute/60' }
}
</script>

<template>
  <PageLayout class="pb-28">
    <PageHeader eyebrow="POS System" title="點餐區">
      <template #action>
        <div class="flex gap-4">
          <RouterLink to="/kitchen" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
            查看備餐 ↗
          </RouterLink>
          <RouterLink to="/pickup" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
            查看取餐 ↗
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <main class="mt-8 flex-1">
      <p v-if="isLoading && stocks.length === 0" class="text-ink-mute animate-pulse">載入商品中...</p>
      <p v-else-if="errorMsg" class="text-danger">{{ errorMsg }}</p>

      <div v-else class="flex flex-col gap-3">
        <div
          v-for="item in stocks"
          :key="item.name"
          class="flex items-stretch overflow-hidden rounded-2xl border border-line bg-surface transition-all duration-200"
          :class="item.soldout ? 'opacity-50 grayscale bg-black/2' : 'hover:border-line-strong shadow-[0_2px_8px_rgba(0,0,0,0.02)]'"
        >
          <div 
            @click="addToCart(item)"
            class="flex flex-1 cursor-pointer flex-col justify-center px-4 py-4 transition-colors active:bg-black/3 sm:px-5"
            :class="item.soldout ? 'cursor-not-allowed pointer-events-none' : ''"
          >
            <div class="flex items-baseline gap-3">
              <span class="text-lg font-bold tracking-tight text-ink">{{ item.name }}</span>
              <span class="text-[13px]" :class="getStockText(item.stock, item.soldout).class">
                {{ getStockText(item.stock, item.soldout).text }}
              </span>
            </div>
            <span class="mt-1 text-sm font-medium text-ink-mute tabular">${{ item.price || 0 }}</span>
          </div>

          <div class="flex min-w-27.5 items-center justify-end gap-3 border-l border-line/50 pr-3 pl-4">
            
            <span 
              class="w-6 text-center text-xl font-bold tabular transition-all duration-200"
              :class="cart[item.name] > 0 ? 'text-ink opacity-100 scale-100' : 'opacity-0 scale-50'"
            >
              {{ cart[item.name] || 0 }}
            </span>

            <button
              @click="removeFromCart(item)"
              :disabled="!cart[item.name]"
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-line bg-paper text-xl font-medium text-ink-mute transition-all hover:text-ink hover:border-line-strong active:scale-90 disabled:opacity-0 disabled:cursor-default"
            >
              −
            </button>
          </div>

        </div>
      </div>
    </main>
  </PageLayout>
</template>