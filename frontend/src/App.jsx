import { Footer } from "./components/Footer"
import { Header } from "./components/Header"
import gramado from "./assets/gramado.jpg"
import { useEffect, useState, useCallback } from "react"
import {PBS01Service} from "./service/PBS01Service"
import { SoccerCard } from "./components/SoccerCard"

function App() {
  const [gameData, setGameData] = useState([])
  const [golCorinthians, setGolCorinthians] = useState(0)
  const [golFlamengo, setGolFlamengo] = useState(0)

   const fetchLastTouch = useCallback(async () => {
    try {
      const data = await PBS01Service.getLastTouch()
      setGameData(prev => [data])
    } catch (error) {
      console.error('Erro ao buscar último toque:', error)
    }
  }, [])

  const fetchGol = useCallback(async () => {
    try {
      const data = await PBS01Service.getGol()
      
      if (data && data.type === 'gol') {
        if (data.team.toLowerCase() === 'flamengo') {
          setGolFlamengo(prev => prev + 1)
        } else if (data.team.toLowerCase() === 'corinthians') {
          setGolCorinthians(prev => prev + 1)
        }
        
        setGameData(prev => [data])
      }
    } catch (error) {
      console.error('Erro ao buscar gol:', error)
    }
  }, [])

  useEffect(() => {
    fetchGol()
    fetchLastTouch()

    const golInterval = setInterval(fetchGol, 5000)
    const lastTouchInterval = setInterval(fetchLastTouch, 5000)

    return () => {
      clearInterval(lastTouchInterval)
      clearInterval(golInterval)
    }
  }, [fetchLastTouch, fetchGol])

  return (
    <>
      <Header/>
      <main 
        className='relative flex justify-between items-center px-10 md:px-20 lg:px-40'
        style={{ 
          backgroundImage: `url(${gramado})`, 
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          height: '100vh', 
        }}>
        
        <div className="absolute inset-0 bg-black opacity-50"></div> 
        
        <div className="relative z-10 text-white flex justify-between items-center w-full">
          {/* Corinthians - Lado Esquerdo */}
          <div className="text-center transform hover:scale-105 transition-transform duration-300">
            <h2 className='text-8xl lg:text-9xl leading-tight mb-4 font-bold text-red-600 drop-shadow-2xl'>
              {golCorinthians}
            </h2>
            <h2 className='text-4xl lg:text-5xl font-bold font-quando tracking-wider text-white drop-shadow-lg'>
              Corinthians
            </h2>
            <div className="w-24 h-1 bg-red-600 mx-auto mt-4 rounded-full"></div>
          </div>

          <div className="mx-12 drop-shadow-2xl">
            {gameData && gameData.length > 0 ? gameData.map((g, index) => (
              <SoccerCard 
                key={index}
                team={g.team}
                name={g.player}
                type={g.type}
              />
            )) : (
              <p className="text-7xl lg:text-8xl font-black text-yellow-400 mx-12 drop-shadow-2xl animate-pulse">x</p>
            )}
          </div>

          <div className="text-center transform hover:scale-105 transition-transform duration-300">
            <h2 className='text-8xl lg:text-9xl leading-tight mb-4 font-bold text-red-600 drop-shadow-2xl'>
              {golFlamengo}
            </h2>
            <h2 className='text-4xl lg:text-5xl font-bold font-quando tracking-wider text-white drop-shadow-lg'>
              Flamengo
            </h2>
            <div className="w-24 h-1 bg-red-600 mx-auto mt-4 rounded-full"></div>
          </div>
        </div>
      </main>
      <Footer/>
    </>
  )
}

export default App