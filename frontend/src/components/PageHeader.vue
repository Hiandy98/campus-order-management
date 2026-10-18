<script setup lang="ts">
defineProps<{
  eyebrow: string
  title: string
}>()
</script>

<template>
  <header class="flex items-start justify-between">
    <div>
      <p class="eyebrow mb-2">{{ eyebrow }}</p>
      <h1 class="text-3xl font-bold tracking-tight text-ink">{{ title }}</h1>
    </div>
    
    <div class="pt-1">
      <slot name="action" />
    </div>
  </header>
</template>