import { onMounted, onUnmounted } from 'vue'

export function useWakeLock() {
  let wakeLock: any = null

  const requestWakeLock = async () => {
    try {
      if ('wakeLock' in navigator) {
        wakeLock = await (navigator as any).wakeLock.request('screen')
        console.log('螢幕常亮已啟用')
      }
    } catch (err: any) {
      console.warn(`無法啟用螢幕常亮: ${err.name}, ${err.message}`)
    }
  }

  const releaseWakeLock = () => {
    if (wakeLock !== null) {
      wakeLock.release()
      wakeLock = null
    }
  }

  const handleVisibilityChange = () => {
    if (document.visibilityState === 'visible') {
      requestWakeLock()
    }
  }

  onMounted(() => {
    requestWakeLock()
    document.addEventListener('visibilitychange', handleVisibilityChange)
  })

  onUnmounted(() => {
    releaseWakeLock()
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  })
}