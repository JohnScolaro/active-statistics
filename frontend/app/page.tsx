"use client";

import ScrollableContentContainer from "@/components/scrollable_content_container";
import SplashPage from "@/components/splash_page";
import TopBarSplashPage from "@/components/top_bar_splash_page";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import RateLimitExceededModal from "@/components/rate_limit_exceeded_modal";
import { useRouter } from "next/navigation";

export default function Index() {
  const searchParams = useSearchParams();
  const [modalState, setModalState] = useState(
    searchParams.get("rate_limit_exceeded") == "true"
  );

  const router = useRouter();

  return (
    <>
      <TopBarSplashPage />
      <ScrollableContentContainer modalState={modalState}>
        <SplashPage />
      </ScrollableContentContainer>
      <RateLimitExceededModal
        handleExit={() => {
          setModalState(false);
          router.push("/");
        }}
        modalState={modalState}
      ></RateLimitExceededModal>
    </>
  );
}
