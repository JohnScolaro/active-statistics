export default function MainContent({ children }: {
    children: React.ReactNode
}) {
    // gap-2
    return <div className="bg-white p-2 m-2 rounded-lg flex flex-col gap-4 overflow-auto" >
        {children}
    </div >

}
