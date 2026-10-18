<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type Order } from '../api'
import { usePolling } from '../usePolling'
import { useSound } from '../composables/useSound'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
import OrderCard from '../components/OrderCard.vue'

const orders = ref<Order[]>([])
const isLoading = ref(true)
const errorMsg = ref('')

const otherActions = ref<{ id: number; pickup_no: string }[]>([])

const { playNewOrder, playAlert } = useSound()

const isCancelSheetOpen = ref(false)
const targetOrderId = ref<number | null>(null)
const CANCEL_REASONS = ['客人跑了', '餐點做錯', '食材沒了', '其他']

let previousIds = new Set<number>()
const processingIds = new Set<number>()

const fetchOrders = async () => {
  try {
    const data = await api.listOrders('pending')
    
    const filteredData = data.filter(o => !processingIds.has(o.id))
    filteredData.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())

    if (!isLoading.value) {
      const currentIds = new Set(filteredData.map((o) => o.id))
      
      const hasNew = filteredData.some((o) => !previousIds.has(o.id))
      if (hasNew && previousIds.size > 0) playNewOrder()

      const removedOrders = orders.value.filter(
        (o) => !currentIds.has(o.id) && !processingIds.has(o.id)
      )
      
      if (removedOrders.length > 0) {
        removedOrders.forEach((o) => {
          if (!otherActions.value.some(a => a.id === o.id)) {
            otherActions.value.push({ id: o.id, pickup_no: String(o.pickup_no) })
          }
        })
        playAlert()
      }

      previousIds = currentIds
    } else {
      previousIds = new Set(filteredData.map((o) => o.id))
    }

    orders.value = filteredData
    errorMsg.value = ''
  } catch (e: any) {
    errorMsg.value = e.message
  } finally {
    isLoading.value = false
  }
}

usePolling(fetchOrders, 2000)

const dismissAction = (id: number) => {
  otherActions.value = otherActions.value.filter(a => a.id !== id)
}

const optimisticRemove = (id: number) => {
  processingIds.add(id)
  const index = orders.value.findIndex((o) => o.id === id)
  if (index === -1) return null
  const removed = orders.value[index]
  orders.value.splice(index, 1)
  previousIds.delete(id)
  return removed
}

const restoreOrder = (order: Order) => {
  processingIds.delete(order.id)
  orders.value.push(order)
  orders.value.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  previousIds.add(order.id)
}

const handleComplete = async (order: Order) => {
  optimisticRemove(order.id)
  try {
    await api.updateStatus(order.id, { status: 'ready' })
  } catch (e: any) {
    if (e.status === 400) return
    alert(`更新失敗：${e.message}`)
    restoreOrder(order)
  }
}

const openCancelSheet = (order: Order) => {
  targetOrderId.value = order.id
  isCancelSheetOpen.value = true
}

const confirmCancel = async (reason: string) => {
  if (targetOrderId.value === null) return
  const order = orders.value.find((o) => o.id === targetOrderId.value)
  if (!order) return

  isCancelSheetOpen.value = false
  optimisticRemove(order.id)

  try {
    await api.updateStatus(order.id, { status: 'cancelled', cancel_reason: reason })
  } catch (e: any) {
    if (e.status === 400) return
    alert(`取消失敗：${e.message}`)
    restoreOrder(order)
  }
}

const pendingCount = computed(() => orders.value.length)
</script>

<template>
  <PageLayout class="pb-10">
    <PageHeader eyebrow="Kitchen Display" title="備餐區">
      <template #action>
        <div class="flex flex-col items-end gap-1">
          <RouterLink to="/" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
            ← 返回點餐
          </RouterLink>
          <span class="text-xs text-ink-soft font-medium">{{ pendingCount }} 筆待處理</span>
        </div>
      </template>
    </PageHeader>

    <main class="mt-8 flex-1">
      
      <div v-if="otherActions.length > 0" class="mb-6 flex flex-col gap-2">
        <p class="eyebrow text-ink-mute">系統通知 (已由其他設備處理)</p>
        <div 
          v-for="action in otherActions" 
          :key="action.id"
          class="flex items-center justify-between rounded-xl border border-line bg-gray-100 p-4"
        >
          <div class="flex items-center gap-3">
            <span class="text-lg font-bold text-ink-mute">#{{ action.pickup_no }}</span>
            <span class="text-sm font-medium text-ink-mute">已由其他人完成或取消</span>
          </div>
          <button 
            @click="dismissAction(action.id)"
            class="rounded-lg bg-surface border border-line px-3 py-1.5 text-sm font-bold text-ink-soft shadow-sm active:scale-95"
          >
            我知道了
          </button>
        </div>
      </div>

      <p v-if="isLoading && orders.length === 0" class="text-ink-mute animate-pulse">載入訂單中...</p>
      <p v-else-if="errorMsg" class="text-danger">{{ errorMsg }}</p>

      <div v-else-if="orders.length === 0 && otherActions.length === 0" class="py-20 text-center">
        <p class="text-2xl font-bold text-ink-mute/50">目前沒有待處理訂單</p>
        <p class="mt-2 text-sm text-ink-mute">新訂單會自動出現在這裡</p>
      </div>

      <div v-else class="flex flex-col gap-4">
        <OrderCard
          v-for="order in orders"
          :key="order.id"
          :order="order"
          complete-label="完成"
          @complete="handleComplete(order)"
          @cancel="openCancelSheet(order)"
        />
      </div>
    </main>

    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isCancelSheetOpen" class="fixed inset-0 z-50 flex items-end justify-center sm:items-center">
        <div @click="isCancelSheetOpen = false" class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative w-full max-w-md rounded-t-2xl bg-surface p-5 shadow-xl sm:rounded-2xl">
          <h3 class="mb-4 text-center text-lg font-bold text-ink">取消原因</h3>
          <div class="flex flex-col gap-2">
            <button
              v-for="reason in CANCEL_REASONS"
              :key="reason"
              @click="confirmCancel(reason)"
              class="w-full rounded-xl py-3.5 text-base font-medium text-ink-soft transition-colors hover:bg-black/5 active:bg-black/10"
            >
              {{ reason }}
            </button>
          </div>
          <div class="mt-4 pt-4 border-t border-line">
            <button
              @click="isCancelSheetOpen = false"
              class="w-full rounded-xl py-3.5 text-base font-bold text-ink-mute transition-colors hover:bg-black/5"
            >
              返回
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </PageLayout>
</template>