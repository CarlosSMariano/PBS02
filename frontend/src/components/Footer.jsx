import logo from '../assets/logos/LogoPassaabola.svg'
import insta from '../assets/icons/instagramLogo.svg'
import youtube from '../assets/icons/youtubeLogo.svg'
import twiter from '../assets/icons/twiterLogo.svg'
import email from '../assets/icons/Email.svg'


export const Footer = () => {
  return (
    <footer className='bg-background-3 text-white'>
      <div className='flex flex-col md:flex-row items-center md:items-start justify-center md:justify-start p-10 gap-6'>


        <div className='flex flex-col md:flex-row w-full md:w-1/2 gap-6 items-center md:items-start justify-center md:justify-between'>
          <img src={logo} alt="Logo" className="w-36 h-30 object-contain" />
          <div className='flex flex-col gap-2 items-center md:items-start text-center md:text-left'>
            <h2 className='text-xl'>Redes Socias</h2>
            <nav>
              <p className='text-gray-400 flex items-center gap-1'><img src={insta} className='w-4 h-4 object-contain' alt="instagram" /> @passaabola</p>
              <p className='text-gray-400 flex items-center gap-1'><img src={youtube} className='w-4 h-4 object-contain' alt="youtube" /> @passaabola</p>
              <p className='text-gray-400 flex items-center gap-1'><img src={twiter} className='w-4 h-4 object-contain' alt="twiter" /> @passaabola</p>
            </nav>
          </div>

          <div className='flex flex-col gap-2 items-center md:items-start'>
            <p className='text-xl'>Contato</p>
            <p className='text-gray-400 flex items-center gap-1'><img src={email} className='w-4 h-4 object-contain' alt="email" /> contato@passabola.com.br</p>
            <button className='bg-btn-accent rounded-xl px-4 py-2 font-bold cursor-pointer'>FALE CONOSCO</button>
          </div>

        </div>
      </div>


<p className='text-sm p-10 relative text-gray-300'>
  <span className="block border-t  border-gray-500 w-full md:hidden mb-2"></span>
  © Copyright 2025. PassaaBola. Todos os direitos reservados
</p>
    </footer>
  )
}