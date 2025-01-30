"use client";

import SideBar from "../components/side_bar/side_bar";
import TopBar from "../components/top_bar";
import { useRouter } from "next/navigation";
import { createContext, useEffect, useState } from "react";
import { wrappedFetch } from "../lib/fetch";

interface DataStatus {
  message: string;
  downloaded: boolean;
}

interface HomeContextType {
  dataStatus: DataStatus;
  setDisabledSidebarSteps: (disabledSidebarSteps: string[]) => void;
  setDataStatus: (dataStatus: DataStatus) => void;
}

export const HomeContext = createContext<HomeContextType>({
  dataStatus: {
    message: "Data status unknown...",
    downloaded: false,
  },
  setDisabledSidebarSteps: (disabledSidebarSteps) => console.log(disabledSidebarSteps),
  setDataStatus: (dataStatus) => console.log(dataStatus),
});

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [disabledSidebarSteps, setDisabledSidebarSteps] = useState(["visualisations"]);
  const [dataStatus, setDataStatus] = useState<DataStatus>({
    message: "Data status unknown...",
    downloaded: false,
  });

  const router = useRouter();

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

    if (!apiUrl) {
      console.error("API base URL is not defined");
      return;
    }

    let intervalId: NodeJS.Timeout | null = null;

    const pollDataStatus = () => {
      wrappedFetch(
        `${apiUrl}/api/data_status`,
        (data: DataStatus) => {
          console.log("Data status fetched:", data);
          setDataStatus(data);

          if (data.downloaded) {
            setDisabledSidebarSteps([]);
            if (intervalId) {
              clearInterval(intervalId); // Stop polling
              intervalId = null;
            }
          }
        },
        (error: any) => {
          console.error("Error fetching data status:", error);
        },
        router
      );
    };

    intervalId = setInterval(pollDataStatus, 3000); // Poll every 3 seconds
    pollDataStatus(); // Initial fetch

    return () => {
      if (intervalId) {
        clearInterval(intervalId); // Cleanup interval on unmount
      }
    };
  }, [router]);

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <HomeContext.Provider
      value={{
        dataStatus,
        setDisabledSidebarSteps,
        setDataStatus,
      }}
    >
      <TopBar sidebarVisible={sidebarVisible} toggleSidebar={toggleSidebar} />
      <div className="flex flex-row p-2 gap-2 grow overflow-auto">
        <SideBar
          sidebarVisible={sidebarVisible}
          toggleSidebar={toggleSidebar}
          disabledSidebarSteps={disabledSidebarSteps}
        />
        <div className="flex bg-white rounded-lg p-2 overflow-auto grow justify-center">
          {children}
        </div>
      </div>
    </HomeContext.Provider>
  );
}
