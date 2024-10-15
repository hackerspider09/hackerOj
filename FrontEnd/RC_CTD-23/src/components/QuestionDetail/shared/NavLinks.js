'use client'

import { Link } from 'react-router-dom'  
// import { usePathname } from "next/navigation";
import React from "react";

const NavLinks = () => {

    // const pathname = usePathname();

  return (
    <div className="flex gap-3">
      {/* <Link href="/learn" className={`${pathname==='/learn' && 'font-medium'}`}>Learn</Link>
      <Link href="/problems" className={`${pathname==='/problems' && 'font-medium'}`}>Problems</Link>
      <Link href="/contests" className={`${pathname==='/contests' && 'font-medium'}`}>Contest</Link>
      <Link href="/interview" className={`${pathname==='/interview' && 'font-medium'}`}>Interview</Link>
      <Link href="/news" className={`${pathname==='/news' && 'font-medium'}`}>News</Link> */}
      <Link href='/'>
            <h2 className='font-bold text-xl'>
              CODEGAMY
            </h2>
          </Link>
          <Link href='/'>
            <h2 className='font-bold text-xl'>
              CODEGAMY
            </h2>
          </Link>
    </div>
  );
};

export default NavLinks;
