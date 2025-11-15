import React from 'react'
import './IdleView.css'

/**
 * F-002: 空闲视图 - 大按钮拨号界面
 */
function IdleView({ onStartCall }) {
  return (
    <div className="idle-view">
      <div className="idle-content">
        {/* 头部信息 */}
        <div className="idle-header">
          <div className="contact-avatar">
            <span className="avatar-text">孙</span>
          </div>
          <h1 className="contact-name">小雅</h1>
          <p className="contact-subtitle">您的AI孙女</p>
        </div>

        {/* 拨号按钮 */}
        <div className="idle-actions">
          <button 
            className="call-button"
            onClick={onStartCall}
          >
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
              <path 
                d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" 
                fill="white"
              />
            </svg>
            <span>呼叫小雅</span>
          </button>

          <p className="hint-text">点击按钮，开始通话</p>
        </div>
      </div>

      {/* 底部装饰 */}
      <div className="idle-footer">
        <p className="footer-text">像打电话一样简单</p>
      </div>
    </div>
  )
}

export default IdleView

