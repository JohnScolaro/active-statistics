export default function ScrollableContentContainer({ children }: {
    children: React.ReactNode
}) {
    return <div className="bg-white p-2 m-2 rounded-lg flex flex-col gap-4 overflow-auto" >
        {children}
    </div >

}
