import type { Metadata } from "next";
import ClientPage from "./client_page";

export const metadata: Metadata = {
  title: "Active Statistics",
  description:
    "Active Statistics is an open source visualiser of Strava data. Connect your Strava account and visualise your data in new and exciting ways.",
  openGraph: {
    title: "Active Statistics",
    description:
      "Active Statistics is an open source visualiser of Strava data. Connect your Strava account and visualise your data in new and exciting ways.",
    url: "https://active-statistics.com/",
    images: [
      {
        url: "https://active-statistics.com/active_statistics_2.png",
        width: 1200,
        height: 630,
        alt: 'A pixelated image with the words "Active Statistics" and then a stick drawing of a person running.',
      },
    ],
  },
};

export default function Index() {
  return <ClientPage />;
}
