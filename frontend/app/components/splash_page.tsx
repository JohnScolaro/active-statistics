import StravaLoginButton from "./strava_login_button";
import Image from "next/image";
import { CanvasGrid } from "../home/[key]/components/animated_polyline_grid/animated_polyline_grid";
import { useState, useEffect } from "react";
import { wrappedFetch } from "../lib/fetch";
import { useRouter } from "next/navigation";

export default function SplashPage() {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [polylines, setPolylines] = useState([]);
  const router = useRouter();

  useEffect(() => {
    wrappedFetch(
      `${apiBaseUrl}/api/example_chart_data`,
      (data) => {
        const polylinesList = data.tab_data.map((item: any) => item.polyline); // Extract polylines
        setPolylines(polylinesList); // Set the extracted polylines
      },
      (error) => console.error("Error fetching example chart data.", error), router
    )
  }, []);

  return (
    <>
      <p>
        Visualise your Strava activities.<br /><br />

        For example, here are all the runs I did in the last year:
      </p>
      <CanvasGrid polylines={polylines} activityType={"Run"} animationTimeMs={5000} showActivityType={false} />
      <p>
        To see this animation with your personal data, log in by clicking the Strava link
        below:
      </p>
      <div className="flex flex-row justify-center">
        <StravaLoginButton />
      </div>
      <hr className="border-0 bg-green-500 min-h-[2px]" />
      <p>
        <b>Frequently asked Questions:</b>
        <br></br>
        <br></br>
        <b className="font-black">What is this?</b>
        <br></br>
        Hi, I&apos;m John! I wanted to visualise data that Strava stores in more ways than
        Strava does. I enjoy data visualisation, exercise, and making websites, so this is
        a fun combination of things I enjoy. I intend to keep this website operational and
        free so long as it doesn&apos;t become prohibatively expensive to maintain!
        <br></br>
        <br></br>
        <b>What do you do with my data?</b>
        <br></br>
        When granted permission, I download all your Strava activity data and use it to
        generate a number of visualisations. After a week I delete it because:</p>

      <ol className="list-disc list-inside ms-4">
        <li>I&apos;m cheap, and don&apos;t want to pay storage costs.</li>
        <li>I don&apos;t want it.</li>
        <li>You can&apos;t leak sensitive data if you just don&apos;t have it.</li>
      </ol>
      <p>
        Don&apos;t worry, I&apos;m not using it for anything nefarious.
        <br></br>
        <br></br>
        <b>I have a cool idea for something to add to your site!</b>
        <br></br>
        Neat! That&apos;s not a question, but feel free to contribute to this website{" "}
        <a className="hyperlink" href="https://github.com/JohnScolaro/active-statistics">
          here
        </a>
        , or if you have any questions or ideas, email me{" "}
        <a className="hyperlink" href="mailto:johnscolaro95@gmail.com">
          here
        </a>
        .<br></br>
        <br></br>
      </p >
      <div className="flex flex-col items-center">
        <Image
          src="/api_logo_pwrdBy_strava_stack_gray.svg"
          width="210"
          height="91"
          alt='Text that says "Powered by Strava"'
          className="h-auto"
        />
      </div>
    </>
  );
}
