import ScrollableContentContainer from '@/components/scollable-content-container'
import SplashPage from '@/components/splash_page'
import TopBarSplashPage from '@/components/top-bar-splash-page'

export default function Index() {

  return (<>
    <TopBarSplashPage />
    <ScrollableContentContainer>
      <SplashPage />
    </ScrollableContentContainer>
  </>)
}
