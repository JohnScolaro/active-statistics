"use client";

import { HomeContext } from "./layout";
import { Spinner } from "../components/spinner/spinner";
import { useContext } from "react";

export default function Page() {
  return (
    <div className="flex flex-col gap-2">
      <WelcomeCard></WelcomeCard>
      <div className="flex flex-col md:flex-row md:justify-items-stretch gap-2">
        <DownloadDataCard />
      </div>
      <MoreInformationCard />
    </div>
  );
}

function WelcomeCard() {
  return (
    <div className="bg-green-200 p-4 rounded-lg text-center">
      <div className="flex flex-col items-center">
        <div className="h-2" />
        <div className="text-xl sm:text-xl lg:text-2xl">
          ✨Welcome to Active Statistics!✨
        </div>
        <div className="h-6" />
        <div className="max-w-80 bg-white p-2 rounded-lg">
          <div className="text-base text-left hidden lg:block">
            👉 Use the buttons on the left to navigate.
          </div>
          <div className="text-base text-left block lg:hidden">
            👉 Use the burger menu to navigate.
          </div>
          <div className="text-base text-left">
            👉 Buttons are disabled until your Strava activities have been downloaded.
          </div>
          <div className="text-base text-left">
            👉 Check your download status below.
          </div>
        </div>
        <div className="h-6" />
      </div>
    </div>
  );
}



function DownloadDataCard() {
  const homeContext = useContext(HomeContext);
  const { dataStatus } = homeContext;

  return (
    <div className="relative md:w-1/2 md:grow">
      <div className="bg-green-200 p-2 rounded-lg">
        <div className="flex flex-col items-center">
          <div className="text-xl sm:text-xl lg:text-2xl">{"Download Data"}</div>
          <div className="h-2" />
          <div>
            <b>Status:</b> {dataStatus.message}
          </div>
          <div className="h-2" />
          <div className="text-8xl">
            {dataStatus.downloaded ? "✅" : <Spinner />}
          </div>
          <div className="h-2" />
        </div>
      </div>
    </div>
  );
}

function MoreInformationCard() {
  return (
    <div className="bg-green-200 p-4 rounded-lg text-center">
      <b>How does this website work?</b>
      <br></br>
      <br></br>
      When you log in, you give this application permission to download your Strava data.
      The website downloads your summary data, and when you click on the tabs on the left, your data is processed to show a bunch of cool stats!
      <br></br>
      <br></br>
      <b>Why does my activity from today not show up?</b>
      <br></br>
      <br></br>
      This application will re-download your data at a maximum of once per week. This is so this application doesn&apos;t hit it&apos;s API limit.
    </div>
  );
}
