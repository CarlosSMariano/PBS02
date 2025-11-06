import logo from '../assets/logos/LogoPassaabola.svg'

export const Header = () => {
  return (
    <header className="flex justify-between items-center p-3 sm:p-4 md:p-4 bg-secondary-2 relative">

      {/* Logo */}
      <div className="flex items-center">
        <img 
          src={logo} 
          alt="Logo Passa a Bola" 
          className="w-6 h-6 sm:w-7 sm:h-7 object-contain" 
        />
      </div>

      {/* Menu Desktop */}
      <div className="flex items-center gap-6 md:gap-20 text-amber-50 font-bold">
        <nav className="hidden md:block">
          <ul className="flex gap-6 md:gap-12 lg:gap-20">
            <li><button className='cursor-pointer'>Notícias</button></li>
            <li><button className='cursor-pointer'>Loja</button></li>

            <li className="relative">
              <button className='cursor-pointer'>Conexões</button>
            </li>

            <li><button className='cursor-pointer'>Sobre</button></li>
          </ul>
        </nav>

        {/* Menu Mobile */}
        <button className="md:hidden text-white text-2xl cursor-pointer">
          ☰
        </button>
      </div>
    </header>
  )
}