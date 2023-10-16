"use client";

export default function Page() {
  return (
    <div className="flex flex-col gap-2">
      <WelcomeCard></WelcomeCard>
      <div className="flex flex-col md:flex-row md:justify-items-stretch gap-2">
        <DownloadDataCard
          message={"Download Summary Data"}
          end_point={"test"}
        ></DownloadDataCard>
        <DownloadDataCard
          message={"Download Detailed Data"}
          end_point={"test"}
        ></DownloadDataCard>
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
          {/* The below instructions are changed depending on if the user is on mobile or not. */}
          <div className="text-base text-left hidden lg:block">
            👉 Use the buttons on the left to navigate.
          </div>
          <div className="text-base text-left block lg:hidden">
            👉 Use the burger menu to navigate.
          </div>

          <div className="text-base text-left">
            👉 Buttons are disabled until your Strava activities have been processed.
          </div>
          <div className="text-base text-left">
            👉 Check your processing status below.
          </div>
        </div>
        <div className="h-6" />
      </div>
    </div>
  );
}

function DownloadDataCard({
  message,
  end_point,
  status,
}: {
  message: string;
  end_point: string;
  status: string;
}) {
  return (
    <div className="bg-green-200 p-2 rounded-lg grow">
      <div className="flex flex-col items-center">
        <div className="text-xl sm:text-xl lg:text-2xl">{message}</div>
        <div className="h-2" />
        <div>
          <b>Status:</b> {status}
        </div>
        <div className="h-2" />
        <div className="text-8xl">✅</div>
        <div className="h-2" />
        <button
          className="p-2 bg-green-400 rounded-lg"
          onClick={() => {
            console.log("yeet");
          }}
        >
          Refresh Data
        </button>
        <div className="h-2" />
      </div>
    </div>
  );
}

// ✅❌✋🔒

function MoreInformationCard() {
  return (
    <div className="bg-green-200 p-4 rounded-lg text-center">
      <b>How does this website work?</b>
      <br></br>
      <br></br>
      When you log in, you give this application permission to download your Strava data.
      When you first log in, the website downloads your summary data, and runs a suite of
      graph and table generating scripts over your activities. The results of these
      scripts are saved, but your activities aren't stored.
      <br></br>
      <br></br>
      <b>Why can't I download my detailed data?</b>
      <br></br>
      <br></br>
      This application has limited access to the Strava API (6000 requests per day) and
      these requests are shared with all the other users of this site. Downloading
      "summary data" for all activities has access to GPS, time, heartrate, and much much
      more, but leaves out some of the more data intensive fields like "Segments" and
      "Best Efforts". Getting a users summary data doesn't use too many requests, so it's
      free for everyone for now. Getting a users detailed data uses so many Strava API
      calls that it's possible for a single user to take down this site for 24 hours, and
      so I've currently turned that feature off. It may return as a paid feature in the
      future.
    </div>
  );
}
