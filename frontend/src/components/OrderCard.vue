<script setup lang="ts">
import { computed } from 'vue'
import type { Order } from '../api'

const props = defineProps<{
  order: Order
  completeLabel: string
}>()

const emit = defineEmits<{
  (e: 'complete'): void
  (e: 'cancel'): void
}>()

const timeStr = computed(() => {
  if (!props.order.created_at) return ''
  const date = new Date(props.order.created_at)
  return date.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit', hour12: false })
})

const itemsList = computed(() => {
  const order = props.order as any
  
  if (order.items && Array.isArray(order.items)) {
    return order.items.map((item: any) => ({
      name: item.name,
      qty: item.quantity || item.qty || 1
    }))
  }
  
  if (order.items_summary) {
    return order.items_summary.split(/[,、，]/).map((s: string) => s.trim())
  }
  
  return []
})
</script>

<template>
  <div class="flex flex-col overflow-hidden rounded-2xl border border-line bg-surface shadow-[0_2px_8px_rgba(0,0,0,0.02)]">
    
    <div class="flex flex-col p-5">
      <div class="flex items-baseline justify-between">
        <div class="flex items-baseline gap-1">
          <span class="text-lg font-bold text-ink-mute">#</span>
          <span class="text-4xl font-black tabular tracking-tight text-ink">{{ order.pickup_no }}</span>
        </div>
        <span class="text-sm font-medium text-ink-mute tabular">{{ timeStr }}</span>
      </div>

      <div class="mt-4 flex flex-col gap-1.5">
        <template v-if="typeof itemsList[0] === 'string'">
          <span 
            v-for="(item, i) in itemsList" 
            :key="i"
            class="text-lg font-medium text-ink-soft leading-snug"
          >
            {{ item }}
          </span>
        </template>
        <template v-else>
          <div 
            v-for="(item, i) in (itemsList as any[])" 
            :key="i"
            class="flex items-baseline justify-between"
          >
            <span class="text-lg font-medium text-ink-soft">{{ item.name }}</span>
            <span class="text-xl font-bold tabular text-ink">× {{ item.qty }}</span>
          </div>
        </template>
      </div>
    </div>

    <div class="flex border-t border-line">
      <button
        @click="emit('complete')"
        class="flex-2 bg-brand py-4 text-lg font-bold text-white transition-all hover:opacity-90 active:bg-brand-press"
      >
        {{ completeLabel }}
      </button>
      <div class="w-px bg-line"></div>
      <button
        @click="emit('cancel')"
        class="flex-1 bg-paper py-4 text-base font-medium text-ink-mute transition-all hover:bg-gray-100 active:bg-gray-200"
      >
        取消
      </button>
    </div>

  </div>
</template>