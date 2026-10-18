<script setup lang="ts">
const tabs = [
  { path: '/', label: '點餐' },
  { path: '/kitchen', label: '備餐' },
  { path: '/pickup', label: '取餐' },
]
</script>

<template>
  <div class="flex min-h-full flex-col bg-gray-100">
    <nav class="sticky top-0 z-10 flex border-b border-gray-200 bg-white">
      <RouterLink
        v-for="t in tabs"
        :key="t.path"
        :to="t.path"
        class="flex-1 py-3 text-center text-base font-bold active:bg-gray-100"
        :class="$route.path === t.path ? 'bg-green-50 text-green-700' : 'text-gray-400'"
      >
        {{ t.label }}
      </RouterLink>
    </nav>

    <main class="flex-1 p-3">
      <RouterView />
    </main>
  </div>
</template>