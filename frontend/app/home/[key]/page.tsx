"use client";

import { CenteredSpinner } from "@/components/spinner/spinner";
import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import Table from "./components/table/table";
import { useRouter } from "next/navigation";
import { wrappedFetch } from "@/lib/fetch";
import ImagePage from "./components/image/image";

export default function Page({ params }: { params: { key: string } }) {
  const [loaded, setLoaded] = useState(false);
  const [data, setData] = useState({});
  const [error, setError] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const url = `/api/data/${params.key}`;
    wrappedFetch(
      url,
      (data) => {
        setData(data);
        setError(data.status != "Success");
        setLoaded(true);
      },
      (err) => {
        setError(true);
        setLoaded(true);
      },
      router
    );
  }, [params.key]);

  if (!loaded) {
    return <CenteredSpinner />;
  }

  if (loaded && error) {
    return <Error />;
  }

  return <PageContentComponent params={params} data={data} />;
}

function PageContentComponent({ params, data }: { params: { key: string }; data: any }) {
  console.log(params);
  console.log(data);
  if (data.type == "PlotTab") {
    return (
      <Plot
        className="grow"
        data={data.tab_data.data}
        layout={data.tab_data.layout}
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
      <div className="flex">
        <Table
          table_data={data.tab_data.table_data}
          show_headings={data.tab_data.show_headings}
          column_info={data.tab_data.columns}
        />
      </div>
    );
  }

  if (data.type == "ImageTab") {
    return <ImagePage data={data.tab_data}></ImagePage>;
  }

  return (
    <>
      <div>Content key: {params.key}</div>
      <br></br>
      <div>{JSON.stringify(data)}</div>
    </>
  );
}

function Error() {
  return (
    <div className="h-full items-center text-center max-w-1/2 pt-[33vh]">
      🚧 Oh no! 🚧
      <br />
      <br />
      Something went wrong! 😭
      <br />
      Feel free to email me and tell me about it{" "}
      <a className="hyperlink" href="mailto:johnscolaro95@gmail.com">
        here
      </a>
      , or fix the code yourself{" "}
      <a className="hyperlink" href="https://github.com/JohnScolaro/active-statistics">
        here!
      </a>
    </div>
  );
}
