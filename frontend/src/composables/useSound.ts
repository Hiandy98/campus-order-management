export function useSound() {
  const playTone = (frequency: number, duration: number, type: OscillatorType = 'sine') => {
    try {
      const AudioContext = window.AudioContext || (window as any).webkitAudioContext
      if (!AudioContext) return
      
      const ctx = new AudioContext()
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()

      osc.type = type
      osc.frequency.setValueAtTime(frequency, ctx.currentTime)
      
      gain.gain.setValueAtTime(0.5, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration)

      osc.connect(gain)
      gain.connect(ctx.destination)

      osc.start()
      osc.stop(ctx.currentTime + duration)
    } catch (e) {
      console.warn('播放音效失敗', e)
    }
  }

  const playNewOrder = () => {
    playTone(880, 0.1, 'sine')
    setTimeout(() => playTone(1320, 0.15, 'sine'), 100)
  }

  const playAlert = () => {
    playTone(330, 0.2, 'triangle')
  }

  return { playNewOrder, playAlert }
}