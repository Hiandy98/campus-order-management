<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type Stock } from '../api'
import { usePolling } from '../usePolling'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
import StockItemCard from '../components/StockItemCard.vue'
import CartDrawer from '../components/CartDrawer.vue'
import SuccessModal from '../components/SuccessModal.vue'

const stocks = ref<Stock[]>([])
const isLoading = ref(true)
const errorMsg = ref('')

const cart = reactive<Record<string, number>>({})
const isCartOpen = ref(false)

const isCheckingOut = ref(false)
const isSuccessModalOpen = ref(false)
const lastPickupNo = ref<number | string | null>(null)

const cartTotalCount = computed(() => Object.values(cart).reduce((a, b) => a + b, 0))
const cartTotalPrice = computed(() => {
  return Object.entries(cart).reduce((sum, [name, qty]) => {
    const item = stocks.value.find((s) => s.name === name)
    return sum + (item?.price || 0) * qty
  }, 0)
})

const fetchStocks = async () => {
  try {
    const data = await api.getStocks()
    
    const savedOrder = JSON.parse(localStorage.getItem('pos_custom_order') || '[]') as string[]
    
    data.sort((a, b) => {
      const indexA = savedOrder.indexOf(a.name)
      const indexB = savedOrder.indexOf(b.name)
      
      const posA = indexA === -1 ? 999 : indexA
      const posB = indexB === -1 ? 999 : indexB
      
      if (posA === 999 && posB === 999) {
        return a.name.localeCompare(b.name)
      }
      return posA - posB
    })
    
    stocks.value = data
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

const clearCart = () => {
  Object.keys(cart).forEach((key) => {
    cart[key] = 0
    delete cart[key]
  })
}

const handleCheckout = async () => {
  if (cartTotalCount.value === 0 || isCheckingOut.value) return
  
  isCheckingOut.value = true
  try {
    const items = Object.entries(cart)
      .filter(([_, quantity]) => quantity > 0)
      .map(([name, quantity]) => ({ name, quantity }))

    const order = await api.createOrder(items)

    lastPickupNo.value = order.pickup_no
    isCartOpen.value = false
    clearCart()
    fetchStocks()
    
    isSuccessModalOpen.value = true

  } catch (e: any) {
    alert(`送出失敗：${e.message}`)
  } finally {
    isCheckingOut.value = false
  }
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

    <SuccessModal
      :is-open="isSuccessModalOpen"
      :pickup-no="lastPickupNo"
      @close="isSuccessModalOpen = false"
    />

  </PageLayout>
</template>