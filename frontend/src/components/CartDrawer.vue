<script setup lang="ts">
import { ref } from 'vue'
import type { Stock } from '../api'

const props = defineProps<{
  cart: Record<string, number>
  stocks: Stock[]
  totalCount: number
  totalPrice: number
  isOpen: boolean
  isCheckingOut?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void
  (e: 'checkout'): void
  (e: 'clear'): void
}>()

const isConfirmingClear = ref(false)

const getPrice = (name: string) => {
  return props.stocks.find((s) => s.name === name)?.price || 0
}

const handleClear = () => {
  emit('clear')
  isConfirmingClear.value = false
  emit('update:isOpen', false)
}
</script>

<template>
  <div class="fixed bottom-0 left-0 right-0 z-40 pointer-events-none">
    
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="isOpen" 
        @click="emit('update:isOpen', false)"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm pointer-events-auto"
      ></div>
    </Transition>

    <div 
      class="relative mx-auto w-full max-w-3xl bg-surface border-t border-line shadow-[0_-4px_20px_rgba(0,0,0,0.05)] transition-transform duration-300 ease-in-out pointer-events-auto"
      :class="isOpen ? 'translate-y-0' : 'translate-y-[calc(100%-72px)]'"
    >
      <div 
        @click="emit('update:isOpen', !isOpen)"
        class="flex h-18 cursor-pointer items-center justify-between px-5 transition-colors hover:bg-black/2"
      >
        <div class="flex items-center gap-3">
          <div class="relative flex h-10 w-10 items-center justify-center rounded-full bg-brand text-white">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="h-5 w-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
            </svg>
            <span v-if="totalCount > 0" class="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-danger text-[10px] font-bold text-white ring-2 ring-surface">
              {{ totalCount }}
            </span>
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-bold text-ink">{{ isOpen ? '收合明細' : '展開明細' }}</span>
            <span class="text-xs text-ink-mute">{{ totalCount }} 件商品</span>
          </div>
        </div>
        <div class="text-right">
          <span class="text-2xl font-bold tabular text-ink">${{ totalPrice }}</span>
        </div>
      </div>

      <div class="max-h-[60vh] overflow-y-auto px-5 pb-6 pt-2 border-t border-line/50 select-none">
        <div v-if="totalCount === 0" class="py-10 text-center text-ink-mute">
          購物車是空的
        </div>
        
        <div v-else class="flex flex-col gap-4">
          <div 
            v-for="(qty, name) in cart" 
            :key="name"
            v-show="qty > 0"
            class="flex items-center justify-between border-b border-line/30 pb-3 last:border-0"
          >
            <div class="flex flex-col">
              <span class="text-base font-bold text-ink">{{ name }}</span>
              <span class="text-sm text-ink-mute tabular">${{ getPrice(name) }} x {{ qty }}</span>
            </div>
            <span class="text-lg font-bold tabular text-ink">
              ${{ getPrice(name) * qty }}
            </span>
          </div>

          <div class="mt-4 flex flex-col gap-4 pt-2">
            
            <div class="flex min-h-8 items-center justify-end">
              <button 
                v-if="!isConfirmingClear"
                @click="isConfirmingClear = true"
                class="text-sm font-medium text-ink-mute transition-colors hover:text-danger"
              >
                清空購物車
              </button>

              <div v-else class="flex items-center gap-3">
                <span class="text-sm font-bold text-danger">確定要清空嗎？</span>
                <button 
                  @click="isConfirmingClear = false"
                  class="rounded-lg px-3 py-1.5 text-sm font-medium text-ink-soft hover:bg-black/5"
                >
                  取消
                </button>
                <button 
                  @click="handleClear"
                  class="rounded-lg bg-danger px-4 py-1.5 text-sm font-bold text-white shadow-sm active:scale-95"
                >
                  確定清空
                </button>
              </div>
            </div>

            <button 
              @click="!isCheckingOut && emit('checkout')"
              :disabled="isCheckingOut"
              class="w-full rounded-xl bg-brand py-4 text-lg font-bold text-white shadow-sm transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isCheckingOut ? '處理中...' : `確認送出 · $${totalPrice}` }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>