import { useState } from 'react'
import LandingPage from './components/LandingPage'
import ChatWidget from './components/ChatWidget'

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <LandingPage onOpenChat={() => setIsChatOpen(true)} />
      <ChatWidget isOpen={isChatOpen} onToggle={() => setIsChatOpen(!isChatOpen)} />
    </div>
  )
}

export default App
