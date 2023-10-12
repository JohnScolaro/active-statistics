'use client'

import '../app/globals.css'
import TopBar from '@/components/top-bar'
import { useRouter, usePathname } from 'next/navigation'
import { getCookie } from 'cookies-next'
import { useEffect, useState, useContext, createContext } from 'react'

const LoggedInContext = createContext(false);

export function useLoggedIn() {
    return useContext(LoggedInContext);
}

export default function Base({
    children,
}: {
    children: React.ReactNode
}) {
    const router = useRouter();
    const [loggedIn, setLoggedIn] = useState(false);
    const pathname = usePathname();

    // Just once, on component load time, check if there is a "logged_in" cookie.
    // Use it to set initial state.
    useEffect(() => {
        console.log('1 ' + pathname);

        setLoggedIn(getCookie('logged_in') == 'true');
    }, [])

    // Every time the logged_in state changes, route to home or the splash page.
    useEffect(() => {
        console.log('2 ' + pathname);

        if (loggedIn && pathname == '/') {
            router.push('/home');
        }

        if (!loggedIn) {
            router.push('/');
        }

    }, [loggedIn]);

    return <LoggedInContext.Provider value={loggedIn}>
        <div className="flex flex-col bg-green-100 h-screen">
            <TopBar loggedIn={loggedIn} />
            {children}
        </div>
    </LoggedInContext.Provider>
}
