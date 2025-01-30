import "./globals.css";
import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import Base from "./components/base";

const roboto = Roboto({ weight: ["400"], subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Active Statistics",
  description: "Visualise your Strava Data in Depth",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={roboto.className}>
        <Base>{children}</Base>
      </body>
    </html>
  );
}
