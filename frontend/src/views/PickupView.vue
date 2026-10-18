<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type Order } from '../api'
import { usePolling } from '../usePolling'
import { useSound } from '../composables/useSound'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
import OrderCard from '../components/OrderCard.vue'

const readyOrders = ref<Order[]>([])
const cancelledOrders = ref<Order[]>([])
const isLoading = ref(true)
const errorMsg = ref('')

const { playNewOrder, playAlert } = useSound()

const HIDDEN_KEY = 'pos_hidden_cancelled_ids'
let hiddenIds = new Set<number>(JSON.parse(localStorage.getItem(HIDDEN_KEY) || '[]'))

let previousReadyIds = new Set<number>()
let previousCancelledIds = new Set<number>()

const processingIds = new Set<number>()

const fetchOrders = async () => {
  try {
    const [readyData, cancelledData] = await Promise.all([
      api.listOrders('ready'),
      api.listOrders('cancelled')
    ])
    
    const filteredReady = readyData.filter(o => !processingIds.has(o.id))
    
    filteredReady.sort((a, b) => {
      const timeA = new Date(a.ready_at || a.created_at).getTime()
      const timeB = new Date(b.ready_at || b.created_at).getTime()
      return timeA - timeB
    })

    const validCancelled = cancelledData
      .filter((o) => !hiddenIds.has(o.id))
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

    if (!isLoading.value) {
      const hasNewReady = filteredReady.some((o) => !previousReadyIds.has(o.id))
      if (hasNewReady && previousReadyIds.size > 0) playNewOrder()

      const hasNewCancel = validCancelled.some((o) => !previousCancelledIds.has(o.id))
      if (hasNewCancel && previousCancelledIds.size > 0) playAlert()
    }
    
    previousReadyIds = new Set(filteredReady.map((o) => o.id))
    previousCancelledIds = new Set(validCancelled.map((o) => o.id))

    readyOrders.value = filteredReady
    cancelledOrders.value = validCancelled
    errorMsg.value = ''
  } catch (e: any) {
    errorMsg.value = e.message
  } finally {
    isLoading.value = false
  }
}

usePolling(fetchOrders, 3000)

const hideCancelledOrder = (id: number) => {
  hiddenIds.add(id)
  localStorage.setItem(HIDDEN_KEY, JSON.stringify(Array.from(hiddenIds)))
  cancelledOrders.value = cancelledOrders.value.filter((o) => o.id !== id)
}

const optimisticRemove = (id: number) => {
  processingIds.add(id)
  const index = readyOrders.value.findIndex((o) => o.id === id)
  if (index === -1) return null
  const removed = readyOrders.value[index]
  readyOrders.value.splice(index, 1)
  previousReadyIds.delete(id)
  return removed
}

const restoreOrder = (order: Order) => {
  processingIds.delete(order.id)
  readyOrders.value.push(order)
  readyOrders.value.sort((a, b) => new Date(a.ready_at || a.created_at).getTime() - new Date(b.ready_at || b.created_at).getTime())
  previousReadyIds.add(order.id)
}

const handleComplete = async (order: Order) => {
  optimisticRemove(order.id)
  try {
    await api.updateStatus(order.id, { status: 'completed' })
  } catch (e: any) {
    if (e.status === 400) return
    alert(`更新失敗：${e.message}`)
    restoreOrder(order)
  }
}

const handleCancelDirectly = async (order: Order) => {
  optimisticRemove(order.id)
  try {
    await api.updateStatus(order.id, { status: 'cancelled', cancel_reason: '取餐區取消' })
  } catch (e: any) {
    if (e.status === 400) return
    alert(`取消失敗：${e.message}`)
    restoreOrder(order)
  }
}

const totalCount = computed(() => readyOrders.value.length + cancelledOrders.value.length)
</script>

<template>
  <PageLayout class="pb-10">
    <PageHeader eyebrow="Pickup Display" title="取餐區">
      <template #action>
        <div class="flex flex-col items-end gap-1">
          <RouterLink to="/" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
            ← 返回點餐
          </RouterLink>
          <span class="text-xs text-ink-soft font-medium">{{ readyOrders.length }} 筆待取餐</span>
        </div>
      </template>
    </PageHeader>

    <main class="mt-8 flex-1">
      <p v-if="isLoading && totalCount === 0" class="text-ink-mute animate-pulse">載入訂單中...</p>
      <p v-else-if="errorMsg" class="text-danger">{{ errorMsg }}</p>

      <div v-else-if="totalCount === 0" class="py-20 text-center">
        <p class="text-2xl font-bold text-ink-mute/50">目前沒有待取餐訂單</p>
        <p class="mt-2 text-sm text-ink-mute">備餐完成後會自動出現在這裡</p>
      </div>

      <div v-else class="flex flex-col gap-6">
        <div v-if="cancelledOrders.length > 0" class="flex flex-col gap-3">
          <p class="eyebrow text-danger">已取消 (請確認)</p>
          <div 
            v-for="order in cancelledOrders" 
            :key="'c-' + order.id"
            class="flex items-center justify-between rounded-2xl border border-red-200 bg-red-50 p-5"
          >
            <div class="flex items-baseline gap-2">
              <span class="text-xl font-bold text-red-700">#{{ order.pickup_no }}</span>
              <span class="text-sm font-medium text-red-600/80">{{ order.cancel_reason || '已取消' }}</span>
            </div>
            <button 
              @click="hideCancelledOrder(order.id)"
              class="rounded-lg border border-red-200 bg-white px-4 py-2 text-sm font-bold text-red-600 shadow-sm active:scale-95"
            >
              我知道了
            </button>
          </div>
        </div>

        <div v-if="readyOrders.length > 0" class="flex flex-col gap-4">
          <OrderCard
            v-for="order in readyOrders"
            :key="order.id"
            :order="order"
            complete-label="客人取餐"
            @complete="handleComplete(order)"
            @cancel="handleCancelDirectly(order)"
          />
        </div>
      </div>
    </main>
  </PageLayout>
</template>ㄋ