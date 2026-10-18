<script setup lang="ts">
import type { Stock } from '../api'

const props = defineProps<{
  item: Stock
  quantity: number
}>()

const emit = defineEmits<{
  (e: 'add'): void
  (e: 'remove'): void
}>()

const getStockText = (stock: number, soldout: boolean) => {
  if (soldout || stock <= 0) return { text: '已售完', class: 'text-ink-mute' }
  if (stock <= 10) return { text: `僅剩 ${stock}`, class: 'text-red-500 font-medium' }
  if (stock <= 30) return { text: `剩 ${stock}`, class: 'text-amber-500' }
  return { text: '充足', class: 'text-ink-mute/60' }
}
</script>

<template>
  <div
    class="flex items-stretch overflow-hidden rounded-2xl border border-line bg-surface transition-all duration-200"
    :class="item.soldout ? 'opacity-50 grayscale bg-black/2' : 'hover:border-line-strong shadow-[0_2px_8px_rgba(0,0,0,0.02)]'"
  >
    <div 
      @click="!item.soldout && emit('add')"
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
        :class="quantity > 0 ? 'text-ink opacity-100 scale-100' : 'opacity-0 scale-50'"
      >
        {{ quantity }}
      </span>

      <button
        @click="emit('remove')"
        :disabled="!quantity"
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-line bg-paper text-xl font-medium text-ink-mute transition-all hover:text-ink hover:border-line-strong active:scale-90 disabled:opacity-0 disabled:cursor-default"
      >
        −
      </button>
    </div>
  </div>
</template>