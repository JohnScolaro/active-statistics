'use client'

import SideBarButtons from "@/components/fancy-buttons"

export default function HomeLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        // misc container
        < div className="flex flex-row p-2 gap-2 grow overflow-auto" >
            {/* Sidebar */}
            <div className="w-72 h-full overflow-auto shrink-0 p-2 rounded-lg bg-green-500">
                <SideBarButtons />
            </div>
            {/* Content */}
            <div className="bg-white rounded-lg p-2 h-full overflow-auto grow">
                {children}
            </div>
        </div >
    )
}
