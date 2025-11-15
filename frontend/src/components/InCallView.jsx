import React, { useState, useEffect, useRef } from 'react'
import VoiceActivityDetector from './VoiceActivityDetector'
import './InCallView.css'

/**
 * F-003: 通话中视图 - 像素级复刻iOS通话界面
 */
function InCallView({ callState, onEndCall }) {
  const [duration, setDuration] = useState(0)
  const [isMuted, setIsMuted] = useState(false)
  const [isSpeaker, setIsSpeaker] = useState(true)
  const [isAISpeaking, setIsAISpeaking] = useState(false)
  const audioRef = useRef(null)

  // 通话计时器
  useEffect(() => {
    if (callState === 'connected') {
      const timer = setInterval(() => {
        setDuration(prev => prev + 1)
      }, 1000)
      return () => clearInterval(timer)
    }
  }, [callState])

  // 格式化通话时长
  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // 处理用户语音输入
  const handleUserSpeech = async (audioBlob) => {
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'user_speech.webm')

      const response = await fetch('/api/chat', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        // 获取AI回复的文本（从header，需要URL解码）
        const aiText = decodeURIComponent(response.headers.get('X-AI-Text') || '')
        const userText = decodeURIComponent(response.headers.get('X-User-Text') || '')
        
        console.log('用户:', userText)
        console.log('AI:', aiText)

        // 播放AI语音回复
        const audioBlob = await response.blob()
        const audioUrl = URL.createObjectURL(audioBlob)
        
        if (audioRef.current) {
          audioRef.current.src = audioUrl
          audioRef.current.play()
          setIsAISpeaking(true)
        }
      }
    } catch (error) {
      console.error('通话错误:', error)
    }
  }

  // 音频播放结束
  const handleAudioEnded = () => {
    setIsAISpeaking(false)
  }

  return (
    <div className="in-call-view">
      {/* 顶部状态栏 */}
      <div className="call-status-bar">
        <div className="status-dot" />
        <span className="status-text">
          {callState === 'connecting' && '正在连接...'}
          {callState === 'connected' && formatDuration(duration)}
          {callState === 'ended' && '通话结束'}
        </span>
      </div>

      {/* 联系人信息 */}
      <div className="call-contact-info">
        <div className="call-avatar">
          <span className="avatar-text">孙</span>
          {isAISpeaking && (
            <div className="speaking-indicator">
              <span className="wave"></span>
              <span className="wave"></span>
              <span className="wave"></span>
            </div>
          )}
        </div>
        <h2 className="call-name">小雅</h2>
        <p className="call-subtitle">
          {callState === 'connected' ? '通话中' : '连接中...'}
        </p>
      </div>

      {/* VAD语音活动检测 */}
      {callState === 'connected' && (
        <VoiceActivityDetector 
          onSpeechDetected={handleUserSpeech}
          isEnabled={!isAISpeaking && !isMuted}
        />
      )}

      {/* 控制按钮 */}
      <div className="call-controls">
        <div className="control-row">
          {/* 静音 */}
          <button 
            className={`control-btn ${isMuted ? 'active' : ''}`}
            onClick={() => setIsMuted(!isMuted)}
          >
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <path 
                d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" 
                fill="currentColor"
              />
              <path 
                d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round"
              />
              {isMuted && (
                <line 
                  x1="4" y1="4" x2="20" y2="20" 
                  stroke="currentColor" 
                  strokeWidth="2"
                />
              )}
            </svg>
            <span>{isMuted ? '已静音' : '静音'}</span>
          </button>

          {/* 扬声器 */}
          <button 
            className={`control-btn ${isSpeaker ? 'active' : ''}`}
            onClick={() => setIsSpeaker(!isSpeaker)}
          >
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <path 
                d="M11 5L6 9H2v6h4l5 4V5zM19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              />
            </svg>
            <span>扬声器</span>
          </button>
        </div>

        {/* 挂断按钮 */}
        <button 
          className="end-call-btn"
          onClick={onEndCall}
        >
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
            <path 
              d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" 
              fill="white"
              transform="rotate(135 12 12)"
            />
          </svg>
        </button>
      </div>

      {/* 隐藏的音频播放器 */}
      <audio 
        ref={audioRef}
        onEnded={handleAudioEnded}
      />
    </div>
  )
}

export default InCallView

