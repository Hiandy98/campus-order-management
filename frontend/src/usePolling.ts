import { onMounted, onUnmounted } from 'vue'

export function usePolling(task: () => Promise<void> | void, intervalMs: number) {
  let timer: number | undefined
  let unmounted = false
  let running = false

  const tick = async () => {
    if (running || document.hidden) return
    running = true
    try {
      await task()
    } catch (e) {
      console.error('[polling]', e)
    } finally {
      running = false
    }
  }

  const stop = () => {
    if (timer !== undefined) {
      clearInterval(timer)
      timer = undefined
    }
  }

  const start = () => {
    stop()
    if (unmounted) return
    tick()
    timer = window.setInterval(tick, intervalMs)
  }

  const onVisibility = () => {
    if (document.hidden) stop()
    else start()
  }

  onMounted(() => {
    start()
    document.addEventListener('visibilitychange', onVisibility)
  })

  onUnmounted(() => {
    unmounted = true
    stop()
    document.removeEventListener('visibilitychange', onVisibility)
  })

  return { start, stop }
}