"use client";

import ScrollableContentContainer from "./components/scrollable_content_container";
import SplashPage from "./components/splash_page";
import TopBarSplashPage from "./components/top_bar_splash_page";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import RateLimitExceededModal from "./components/rate_limit_exceeded_modal";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ClientPage() {
    const searchParams = useSearchParams();
    const [modalState, setModalState] = useState(
        searchParams.get("rate_limit_exceeded") == "true",
    );

    const router = useRouter();

    return (
        <>
            <TopBarSplashPage />
            <ScrollableContentContainer>
                <SplashPage />
            </ScrollableContentContainer>
            <RateLimitExceededModal
                handleExit={() => {
                    setModalState(false);
                    router.push("/");
                }}
                modalState={modalState}
            />
            <div className="text-center mb-2">
                Made with ❤️ in{" "}
                <Link className="hyperlink" href="https://en.wikipedia.org/wiki/Brisbane">
                    Brisbane
                </Link>{" "}
                by{" "}
                <Link className="hyperlink" href="https://johnscolaro.xyz">
                    John
                </Link>
            </div>
        </>
    );
}
