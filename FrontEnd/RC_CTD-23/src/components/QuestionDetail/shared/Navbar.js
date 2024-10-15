import { Link } from 'react-router-dom'  
import React from 'react'
// import NavLinks from './NavLinks'

const Navbar =() => {

  return (
    <div className='w-full bg-light-1'>

      <div className='max-w-6xl mx-auto flex justify-between items-center px-2 py-3'>

        <div className='flex justify-between items-center gap-7'>
          <Link href='/'>
            <h2 className='font-bold text-xl'>
              CODEGAMY
            </h2>
          </Link>
          
            {/* <NavLinks /> */}
          </div>

        <div className='flex justify-between items-center gap-7'>
          
              <><Link href='/login'>
                Login
              </Link>
                <Link href='/register'>
                  Register
                </Link></>
            
        </div>
      </div>


    </div>
  )
}

export default Navbar