<script setup lang="ts">
defineProps<{
  isOpen: boolean
  pickupNo: number | string | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()
</script>

<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div 
      v-if="isOpen && pickupNo !== null" 
      @click="emit('close')"
      class="fixed inset-0 z-50 flex cursor-pointer flex-col items-center justify-center bg-brand p-6"
    >
      <p class="eyebrow mb-6 text-brand-ink/70">取餐號碼</p>
      
      <h2 class="text-[140px] font-black leading-none tabular text-brand-ink sm:text-[180px]">
        #{{ pickupNo }}
      </h2>
      
      <p class="mt-16 text-sm font-medium tracking-widest text-brand-ink/50 uppercase">
        Tap anywhere to close
      </p>
    </div>
  </Transition>
</template>