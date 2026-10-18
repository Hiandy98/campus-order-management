<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-5 pt-8 pb-10">
    
    <header class="flex items-start justify-between">
      <div>
        <p class="eyebrow mb-2">Kitchen Display</p>
        <h1 class="text-3xl font-bold tracking-tight text-ink">備餐區</h1>
      </div>
      
      <RouterLink to="/" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors pt-1">
        ← 返回點餐
      </RouterLink>
    </header>

    <main class="mt-12 flex-1">
      <p class="text-ink-mute">取餐區建置中...</p>
    </main>
    
  </div>
</template>