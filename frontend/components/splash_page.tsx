import PlotContainer from "./plot_container";
import StravaLoginButton from "./strava_login_button";
import Image from "next/image";

export default function SplashPage() {
  return (
    <>
      <p>
        Get interesting statistics about your Strava activities for free! Active
        Statistics is an open source data visualisation project. Here is an example plot
        showing personal bests over time:
      </p>
      <PlotContainer dataURL="/api/example_chart_data" />
      <p>
        To see these plots with your personal data, log in by clicking the Strava link
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
        <b>Who are you?</b>
        <br></br>
        I&apos;m John! I wanted to visualise data that Strava stores in more ways than
        Strava does. I enjoy data visualisation, exercise, and making websites so this is
        a fun combination of things I enjoy. I intend to keep this website operational and
        free so long as it doesn&apos;t become prohibatively expensive to maintain!
        <br></br>
        <br></br>
        <b>What do I do with your data?</b>
        <br></br>
        When granted permission, I download all your Strava activity data and use it to
        generate a number of visualisations. Because I&apos;m really cheap, I delete all
        your data after a month of not accessing it to avoid paying money to store data I
        realistically don&apos;t care about. Don&apos;t worry, I&apos;m not using it for
        anything nefarious.
        <br></br>
        <br></br>
        <b>I have a cool idea for something to add to your site!</b>
        <br></br>
        Neat! That&apos;s not a question, but feel free to contribute to this website{" "}
        <a className="hyperlink" href="https://github.com/JohnScolaro/active-statistics">
          here
        </a>
        , or if you have any other questions, email me{" "}
        <a className="hyperlink" href="mailto:johnscolaro95@gmail.com">
          here
        </a>
        .<br></br>
        <br></br>
      </p>
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
