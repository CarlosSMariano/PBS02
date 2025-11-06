import { Footer } from "./components/Footer"
import { Header } from "./components/Header"
import gramado from "./assets/gramado.jpg"
import { useEffect, useState } from "react"
import {PBS01Service} from "./service/PBS01Service"

function App() {
  const [newsGame, setNewsGame] = useState([])

  useEffect(() => {
    const fetchLastTouch = async () => {
      const data = await PBS01Service.getLastTouch()
      setNewsGame(data)
    }
    const fetchGol = async () => {
      const data = await PBS01Service.getGol()
      setNewsGame(data)
    }

    fetchLastTouch()
  }, [])

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
              1
            </h2>
            <h2 className='text-4xl lg:text-5xl font-bold font-quando tracking-wider text-white drop-shadow-lg'>
              Corinthians
            </h2>
            <div className="w-24 h-1 bg-red-600 mx-auto mt-4 rounded-full"></div>
          </div>

          <div className="mx-12 drop-shadow-2xl">
            x
          </div>

          <div className="text-center transform hover:scale-105 transition-transform duration-300">
            <h2 className='text-8xl lg:text-9xl leading-tight mb-4 font-bold text-red-600 drop-shadow-2xl'>
              0
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