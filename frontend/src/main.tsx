import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import VireonApp from './VireonApp'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <VireonApp />
  </StrictMode>,
)
