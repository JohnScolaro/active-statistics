import ScrollableContentContainer from '@/components/scrollable_content_container'
import SplashPage from '@/components/splash_page'
import TopBarSplashPage from '@/components/top_bar_splash_page'

export default function Index() {

  return (<>
    <TopBarSplashPage />
    <ScrollableContentContainer>
      <SplashPage />
    </ScrollableContentContainer>
  </>)
}
