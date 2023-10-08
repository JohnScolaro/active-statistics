import Image from 'next/image'
import { getUrl } from '@/lib/links'

export default function StravaLoginButton() {
    /*
    Arguably this shouldn't be hard coded, but I don't want to rely on
    another Strava library since I'm already relying on Stravalib on the
    backend. I'll figure out something better to do later.
    */
    const redirect_uri = getUrl('authenticate');
    const link = `https://www.strava.com/oauth/authorize?client_id=106254&amp;redirect_uri=${redirect_uri}&amp;approval_prompt=auto&amp;scope=read%2Cactivity%3Aread&amp;response_type=code`;
    return <a href={link}>
        <Image src="/btn_strava_connectwith_orange.svg" width={193} height={48} alt='Text saying: "Connect with Strava"' className='h-auto' />
    </a>
}
