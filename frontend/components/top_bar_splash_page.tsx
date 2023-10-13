'use client'

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function TopBarSplashPage() {
    return (
        <div className="bg-green-600 flex justify-between p-2 mt-2 ml-2 mr-2 rounded-lg h-14" >
            < Link href="/" className='text-white text-2xl font-bold'><span className='align-middle'>Active Statistics</span></Link >
            <a href="https://github.com/JohnScolaro/active-statistics">
                <Image src="/github-mark-white.svg" width={0} height={0} alt='GitHub Logo' className='w-auto h-full' />
            </a>
        </div >
    );
}
