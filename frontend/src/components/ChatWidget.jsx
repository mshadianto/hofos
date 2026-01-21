import { useState, useRef, useEffect } from 'react'

const ChatWidget = ({ isOpen, onToggle }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: '🚗 *SELAMAT DATANG DI HONDA FREED SUPERCHATBOT!*\n_Developed by MS Hadianto #1347_\n\nSaya asisten AI khusus untuk Honda Freed GB3/GB4 (2008-2016).\n\nKetik keluhan atau kirim foto masalah mobil Anda!'
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const fileInputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const formatMessage = (text) => {
    return text
      .replace(/\*([^*]+)\*/g, '<strong>$1</strong>')
      .replace(/_([^_]+)_/g, '<em>$1</em>')
      .replace(/\n/g, '<br/>')
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Ukuran file maksimal 5MB')
        return
      }
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const clearImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const sendMessage = async () => {
    if ((!inputText.trim() && !selectedImage) || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputText || '📷 [Mengirim gambar untuk diagnosa...]',
      image: imagePreview
    }

    setMessages(prev => [...prev, userMessage])
    const messageText = inputText
    const imageData = imagePreview
    setInputText('')
    clearImage()
    setIsLoading(true)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || '/api'

      let response
      if (imageData) {
        // Send with image
        response = await fetch(`${apiUrl}/process-image`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_API_SECRET || ''}`
          },
          body: JSON.stringify({
            user_id: 'web-' + Date.now(),
            message: messageText || 'Tolong diagnosa masalah dari gambar ini',
            image_base64: imageData.split(',')[1]
          })
        })
      } else {
        // Send text only
        response = await fetch(`${apiUrl}/process`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_API_SECRET || ''}`
          },
          body: JSON.stringify({
            user_id: 'web-' + Date.now(),
            message: messageText
          })
        })
      }

      if (!response.ok) {
        throw new Error('API request failed')
      }

      const data = await response.json()

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.response
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: '⚠️ Maaf, terjadi kesalahan. Silakan coba lagi.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const quickReplies = [
    'Halo',
    'CVT getar',
    'Stage 1',
    'AC tidak dingin'
  ]

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        onClick={onToggle}
        className={`fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all z-50 ${
          isOpen ? 'bg-gray-600 hover:bg-gray-700' : 'bg-whatsapp hover:bg-whatsapp-dark'
        }`}
      >
        {isOpen ? (
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>
            <path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
          </svg>
        )}
      </button>

      {/* Chat Window */}
      <div
        className={`fixed bottom-24 right-6 w-[380px] max-w-[calc(100vw-48px)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden transition-all duration-300 z-50 ${
          isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
        }`}
        style={{ height: '550px', maxHeight: 'calc(100vh - 150px)' }}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-whatsapp-dark to-whatsapp p-4 text-white">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <span className="text-xl">🚗</span>
            </div>
            <div>
              <h3 className="font-semibold">Freed Superchatbot</h3>
              <p className="text-xs text-white/80">AI Mechanic • Vision Enabled</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-2 ${
                  message.type === 'user'
                    ? 'bg-whatsapp text-white rounded-br-md'
                    : 'bg-white text-gray-800 shadow-sm rounded-bl-md'
                }`}
              >
                {message.image && (
                  <img
                    src={message.image}
                    alt="Uploaded"
                    className="max-w-full rounded-lg mb-2"
                    style={{ maxHeight: '150px' }}
                  />
                )}
                <p
                  className="text-sm whitespace-pre-wrap"
                  dangerouslySetInnerHTML={{ __html: formatMessage(message.text) }}
                />
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Image Preview */}
        {imagePreview && (
          <div className="px-4 py-2 bg-gray-100 border-t">
            <div className="relative inline-block">
              <img
                src={imagePreview}
                alt="Preview"
                className="h-20 rounded-lg"
              />
              <button
                onClick={clearImage}
                className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Quick Replies */}
        {messages.length <= 2 && !imagePreview && (
          <div className="px-4 py-2 bg-gray-50 border-t flex gap-2 overflow-x-auto">
            {quickReplies.map((reply) => (
              <button
                key={reply}
                onClick={() => {
                  setInputText(reply)
                  setTimeout(() => sendMessage(), 100)
                }}
                className="px-3 py-1 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:bg-gray-100 whitespace-nowrap"
              >
                {reply}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <div className="p-4 bg-white border-t">
          <div className="flex gap-2 items-center">
            {/* Image Upload Button */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
              disabled={isLoading}
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="w-10 h-10 text-gray-500 hover:text-whatsapp hover:bg-gray-100 rounded-full flex items-center justify-center transition-colors disabled:opacity-50"
              title="Kirim gambar"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </button>

            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={imagePreview ? "Tambah deskripsi (opsional)..." : "Ketik atau kirim foto..."}
              className="flex-1 px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-whatsapp"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={(!inputText.trim() && !selectedImage) || isLoading}
              className="w-10 h-10 bg-whatsapp hover:bg-whatsapp-dark disabled:bg-gray-300 text-white rounded-full flex items-center justify-center transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default ChatWidget
