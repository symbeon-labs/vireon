import { useState } from 'react'
import './neural-styles.css'
import NeuralDashboard from './components/NeuralDashboard'

function VireonApp() {
  const [darkMode, setDarkMode] = useState(false)

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  return (
    <div className={darkMode ? 'dark' : ''}>
      <button 
        className="fixed top-4 right-4 z-50 px-3 py-2 rounded-full bg-secondary text-secondary-foreground" 
        onClick={toggleDarkMode}
      >
        {darkMode ? 'Modo Claro' : 'Modo Escuro'}
      </button>
      <NeuralDashboard />
    </div>
  )
}

export default VireonApp
