import TopBar from "@/components/top-bar"
import MainContent from "@/components/main-content"

export default function Home() {
    return (
        <main>
            <div className="flex flex-col bg-green-100 h-screen">
                <TopBar showBurgerMenu={true} />
                <MainContent>
                    <p>
                        Lorem Ispum or some other bullshit
                    </p>
                </MainContent>
            </div>
        </main >
    )
}
