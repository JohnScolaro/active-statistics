'use client'

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import SideMenu from './side-menu';

interface TopBarProps {
    loggedIn: boolean;
}

export default function TopBar({ loggedIn }: TopBarProps) {
    const [isMenuOpen, setMenuOpen] = useState(false);

    const toggleMenu = () => {
        setMenuOpen(!isMenuOpen);
    };

    return (
        <div className="bg-green-600 flex justify-between p-2 mt-2 ml-2 mr-2 rounded-lg h-14" >
            {loggedIn && (
                <button className="burger-menu" onClick={toggleMenu}>
                    &#9776;
                </button>
            )}
            < Link href="/" className='text-white text-2xl font-bold'><span className='align-middle'>Active Statistics</span></Link >
            <a href="https://github.com/JohnScolaro/active-statistics">
                <Image src="/github-mark-white.svg" width={0} height={0} alt='GitHub Logo' className='w-auto h-full' />
            </a>
            {loggedIn && <SideMenu isOpen={isMenuOpen} onClose={toggleMenu} />}
        </div >
    );
}