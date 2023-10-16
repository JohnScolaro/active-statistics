"use client";

import { CenteredSpinner } from "@/components/spinner/spinner";
import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Table from "./components/table/table";

export default function Page({ params }: { params: { key: string } }) {
  const [loaded, setLoaded] = useState(false);
  const [data, setData] = useState({});
  const [error, setError] = useState(false);

  useEffect(() => {
    const url = `/api/data/${params.key}`;
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoaded(true);
      })
      .catch((err) => {
        setError(true);
        setLoaded(true);
      });
  }, []);

  if (!loaded) {
    return <CenteredSpinner />;
  }

  if (loaded && error) {
    return <CringeError />;
  }

  return <PageContentComponent params={params} data={data} />;
}

function PageContentComponent({ params, data }: { params: { key: string }; data: any }) {
  if (data.type == "PlotTab") {
    return (
      <Plot
        className="w-full h-full"
        data={data.chart_json.data}
        layout={data.chart_json.layout}
        config={{
          responsive: false,
          displayModeBar: false,
          displaylogo: false,
          showTips: true,
        }}
        useResizeHandler
      />
    );
  }

  if (data.type == "TriviaTab" || data.type == "TableTab") {
    return (
      <Table
        table_data={data.chart_json.table_data}
        show_headings={data.chart_json.show_headings}
        column_info={data.chart_json.columns}
      />
    );
  }

  return (
    <>
      <div>Content key: {params.key}</div>
      <br></br>
      <div>{JSON.stringify(data)}</div>
    </>
  );
}

function CringeError() {
  return (
    <div className="h-full items-center text-center max-w-1/2 mt-[33vw]">
      OOPSIE 🙈 WOOPSIE!!
      <br />
      <br />
      Uwu 💦😋😍 We made 👉 a fucky 🐛 wucky 😤👌🔥!!
      <br />
      The code 🚱 monkeys 🐒🙉🙈 are working 😩😫💪 VEWY 😟 HAWD 🍆 to fix 🔧 this!
    </div>
  );
}
