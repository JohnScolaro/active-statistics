'use client'

import SideBarButtons from "@/components/fancy_buttons"
import TopBar from "@/components/top_bar"
import { useState } from "react"

export default function HomeLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const [sidebarVisible, setSidebarVisible] = useState(false);

    const toggleSidebar = () => {
        setSidebarVisible(!sidebarVisible);
    };

    return (
        <>
            <TopBar burgerMenuFunction={toggleSidebar} />
            <div className="flex flex-row p-2 gap-2 grow overflow-auto" >
                {/* Sidebar */}
                <div className={`w-72 h-full overflow-auto shrink-0 p-2 rounded-lg bg-green-500 ${sidebarVisible ? 'block fixed' : 'hidden'} lg:block`}>
                    <SideBarButtons />
                </div>
                {/* Content */}
                <div className="bg-white rounded-lg p-2 h-full overflow-auto grow">
                    {children}
                </div>
            </div >
        </>
    )
}
