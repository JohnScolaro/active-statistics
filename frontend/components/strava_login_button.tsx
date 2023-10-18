"use client";

import Image from "next/image";
import { useLoggedIn } from "@/components/base";
import Link from "next/link";

export default function StravaLoginButton() {
  const logged_in = useLoggedIn();

  // If we have logged in, make this button navigate us to the /home page.
  // Otherwise it can take us to Strava.
  if (logged_in) {
    return (
      <Link href="/home">
        <Image
          src="/btn_strava_connectwith_orange.svg"
          width={193}
          height={48}
          alt='Text saying: "Connect with Strava"'
          className="h-auto"
        />
      </Link>
    );
  } else {
    /*
        Arguably this shouldn't be hard coded, but I don't want to rely on
        another Strava library since I'm already relying on Stravalib on the
        backend, and I don't want to query the backend for something that should
        obviously be static, so I'm just hardcoding it. I'll figure out something
        better to do later.
        */
    const hostname = window.location.hostname;
    const port = window.location.port;
    const protocol = window.location.protocol;
    const portSuffix = port && port !== "" ? `:${port}` : "";
    const authenticateRoute = `${protocol}//${hostname}${portSuffix}/api/authenticate`;

    const link = `https://www.strava.com/oauth/authorize?client_id=106254&amp;redirect_uri=${authenticateRoute}&amp;approval_prompt=auto&amp;scope=read%2Cactivity%3Aread&amp;response_type=code`;
    return (
      <a href={link}>
        <Image
          src="/btn_strava_connectwith_orange.svg"
          width={193}
          height={48}
          alt='Text saying: "Connect with Strava"'
          className="h-auto"
        />
      </a>
    );
  }
}
