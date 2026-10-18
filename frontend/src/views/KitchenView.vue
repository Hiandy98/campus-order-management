<script setup lang="ts">
import { RouterLink } from 'vue-router'
import PageLayout from '../components/PageLayout.vue'
import PageHeader from '../components/PageHeader.vue'
</script>

<template>
  <PageLayout>
    <PageHeader eyebrow="Kitchen Display" title="備餐區">
      <template #action>
        <RouterLink to="/" class="text-sm font-medium text-ink-mute hover:text-ink transition-colors">
          ← 返回點餐
        </RouterLink>
      </template>
    </PageHeader>

    <main class="mt-12 flex-1">
      <p class="text-ink-mute">備餐區建置中...</p>
    </main>
  </PageLayout>
</template>