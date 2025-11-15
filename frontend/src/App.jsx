import React, { useState } from 'react'
import IdleView from './components/IdleView'
import InCallView from './components/InCallView'
import './App.css'

function App() {
  // F-001: 状态机 - 两个核心状态
  const [isCalling, setIsCalling] = useState(false)
  const [callState, setCallState] = useState('idle') // idle | connecting | connected | ended

  const handleStartCall = () => {
    setIsCalling(true)
    setCallState('connecting')
    
    // 模拟连接过程
    setTimeout(() => {
      setCallState('connected')
      // TODO: 触发AI开场白
    }, 1500)
  }

  const handleEndCall = () => {
    setCallState('ended')
    setTimeout(() => {
      setIsCalling(false)
      setCallState('idle')
    }, 500)
  }

  return (
    <div className="app">
      {!isCalling ? (
        <IdleView onStartCall={handleStartCall} />
      ) : (
        <InCallView 
          callState={callState}
          onEndCall={handleEndCall}
        />
      )}
    </div>
  )
}

export default App

