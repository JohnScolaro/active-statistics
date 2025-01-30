"use client";

import Image from "next/image";
import { useLoggedIn } from "../components/base";
import Link from "next/link";
import { useEffect } from "react";
import { getCookie } from "cookies-next";

export default function StravaLoginButton() {
  const { loggedIn, setLoggedIn } = useLoggedIn();

  // Since the `Base` component only renders initially and never changes, the
  // cookies are never checked again. In the off chance that cookies are
  // deleted mid session, we want this button to check for cookies again when
  // it's displayed, because otherwise clicking it will bounce between /home
  // and / as it get instantly redirected due to not being logged in.
  useEffect(() => {
    const isLoggedIn = getCookie("logged_in") == "true";
    setLoggedIn(isLoggedIn);
  });

  // If we have logged in, make this button navigate us to the /home page.
  // Otherwise it can take us to Strava.
  if (loggedIn) {
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
    let port = window.location.port;

    // For debugging:
    if (hostname == "localhost") {
      port = "8000";
    }

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
