<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type Stock } from '../api'
import { usePolling } from '../usePolling'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
import StockItemCard from '../components/StockItemCard.vue'
import CartDrawer from '../components/CartDrawer.vue'

const stocks = ref<Stock[]>([])
const isLoading = ref(true)
const errorMsg = ref('')

const cart = reactive<Record<string, number>>({})
const isCartOpen = ref(false)

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

const handleCheckout = () => {
  if (cartTotalCount.value === 0) return
  alert('準備送出訂單 下一階段接 API')
  isCartOpen.value = false
}

const clearCart = () => {
  Object.keys(cart).forEach((key) => {
    cart[key] = 0
    delete cart[key]
  })
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
        <StockItemCard
          v-for="item in stocks"
          :key="item.name"
          :item="item"
          :quantity="cart[item.name] || 0"
          @add="addToCart(item)"
          @remove="removeFromCart(item)"
        />
      </div>
    </main>

    <CartDrawer
      v-model:is-open="isCartOpen"
      :cart="cart"
      :stocks="stocks"
      :total-count="cartTotalCount"
      :total-price="cartTotalPrice"
      @checkout="handleCheckout"
      @clear="clearCart"
    />

  </PageLayout>
</template>