/*
A simple component that wraps a plotly plot. It's given a URL to hit, and it
shows a spinner until the plot loads, then it shows the plot. It needs to run
in the client because that's a requirement of plotly.
*/

"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { CenteredSpinner } from "./spinner/spinner";
import { wrappedFetch } from "../lib/fetch";

import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), {
  ssr: false,
});

interface PlotComponentProps {
  dataURL: string;
}

export default function PlotContainer({ dataURL }: PlotComponentProps) {
  const [plotData, setPlotData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Fetch data from the provided URL
    wrappedFetch(
      dataURL,
      (data) => {
        setPlotData(data);
        setIsLoading(false);
      },
      (err) => {
        console.log(err);
        setError(err);
        setIsLoading(false);
      },
      router
    );
  }, [dataURL, router]);

  if (isLoading) {
    return (
      <div className="flex flex-row justify-center">
        <div className="rounded-lg border-green-500 border-2 h-96 max-h-96 w-full max-w-3xl p-2">
          <CenteredSpinner />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-row justify-center">
        <div className="rounded-lg border-red-500 border-2 h-96 max-h-96 w-full max-w-3xl p-2">
          <div className="flex h-full flex-col justify-center text-center">
            <p>
              <b>Oh no, something went wrong! 😔</b>
              <br />
              <br />
              This could have occurred because this is a heartrate plot, but you
              don&apos;t have Strava Premium. Alternatively, it could just be a bug in my
              data processing. Help me fix my code{" "}
              <a
                className="hyperlink"
                href="https://github.com/JohnScolaro/active-statistics"
              >
                here!
              </a>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-row justify-center">
      <div className="rounded-lg border-green-500 border-2  h-96 max-h-96 w-full max-w-3xl p-2">
        <Plot
          className="w-full h-full"
          data={plotData.data}
          layout={plotData.layout}
          config={{
            responsive: false,
            displayModeBar: false,
            displaylogo: false,
            showTips: true,
          }}
          useResizeHandler
        />
      </div>
    </div>
  );
}
