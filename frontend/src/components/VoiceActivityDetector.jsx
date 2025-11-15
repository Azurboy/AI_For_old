import React, { useEffect, useRef, useState } from 'react'
import './VoiceActivityDetector.css'

/**
 * F-004: 语音活动检测 (VAD)
 * 自动检测用户说话，无需"按住说话"
 */
function VoiceActivityDetector({ onSpeechDetected, isEnabled }) {
  const [isListening, setIsListening] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const silenceTimerRef = useRef(null)
  const recordingChunksRef = useRef([])

  useEffect(() => {
    if (!isEnabled) {
      stopListening()
      return
    }

    startListening()

    return () => {
      stopListening()
    }
  }, [isEnabled])

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      })

      // 创建音频上下文
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)
      analyserRef.current.fftSize = 2048

      // 创建MediaRecorder
      mediaRecorderRef.current = new MediaRecorder(stream)
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordingChunksRef.current.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(recordingChunksRef.current, { type: 'audio/webm' })
        recordingChunksRef.current = []
        
        // 只发送大于1秒的录音
        if (audioBlob.size > 10000) {
          onSpeechDetected(audioBlob)
        }
      }

      setIsListening(true)
      detectVoiceActivity()

    } catch (error) {
      console.error('无法访问麦克风:', error)
      alert('请允许访问麦克风以使用语音功能')
    }
  }

  const stopListening = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
    }

    if (audioContextRef.current) {
      audioContextRef.current.close()
    }

    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current)
    }

    setIsListening(false)
    setIsRecording(false)
  }

  const detectVoiceActivity = () => {
    if (!analyserRef.current) return

    const bufferLength = analyserRef.current.fftSize
    const dataArray = new Uint8Array(bufferLength)

    const checkAudio = () => {
      if (!isEnabled || !analyserRef.current) return

      analyserRef.current.getByteTimeDomainData(dataArray)

      // 计算音量
      let sum = 0
      for (let i = 0; i < bufferLength; i++) {
        const value = (dataArray[i] - 128) / 128.0
        sum += value * value
      }
      const volume = Math.sqrt(sum / bufferLength)

      // VAD阈值（可调整）
      const VOICE_THRESHOLD = 0.02
      const SILENCE_DURATION = 1500 // 1.5秒无声后停止录音

      if (volume > VOICE_THRESHOLD) {
        // 检测到声音
        if (!isRecording) {
          console.log('🎤 开始录音')
          setIsRecording(true)
          recordingChunksRef.current = []
          mediaRecorderRef.current.start()
        }

        // 清除静音计时器
        if (silenceTimerRef.current) {
          clearTimeout(silenceTimerRef.current)
        }

        // 设置新的静音计时器
        silenceTimerRef.current = setTimeout(() => {
          if (isRecording && mediaRecorderRef.current.state === 'recording') {
            console.log('⏸️ 停止录音（静音）')
            mediaRecorderRef.current.stop()
            setIsRecording(false)
            
            // 重新开始监听
            setTimeout(() => {
              if (mediaRecorderRef.current && isEnabled) {
                mediaRecorderRef.current.start()
              }
            }, 100)
          }
        }, SILENCE_DURATION)
      }

      requestAnimationFrame(checkAudio)
    }

    checkAudio()
  }

  return (
    <div className="vad-indicator">
      {isListening && (
        <>
          <div className={`vad-status ${isRecording ? 'recording' : 'listening'}`}>
            <div className="vad-dot" />
            <span>{isRecording ? '正在聆听您说话...' : '等待您说话'}</span>
          </div>
          {isRecording && (
            <div className="vad-animation">
              <div className="vad-bar"></div>
              <div className="vad-bar"></div>
              <div className="vad-bar"></div>
              <div className="vad-bar"></div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default VoiceActivityDetector

