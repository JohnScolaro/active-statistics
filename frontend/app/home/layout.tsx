"use client";

import SideBar from "@/components/side_bar/side_bar";
import TopBar from "@/components/top_bar";
import { createContext, useEffect, useState } from "react";
import { finished } from "stream";

interface DataStatus {
  message: string;
  status: string;
  stopPolling: boolean;
}

interface HomeContextType {
  detailedDataStatus: DataStatus;
  summaryDataStatus: DataStatus;
  paidUser: {
    paid: boolean;
  };
  setDisabledSidebarSteps: (disabledSidebarSteps: string[]) => void;
  setSummaryDataStatus: (dataStatus: DataStatus) => void;
  setDetailedDataStatus: (dataStatus: DataStatus) => void;
}

export const HomeContext = createContext<HomeContextType>({
  detailedDataStatus: {
    message: "Data status unknown...",
    status: "unknown",
    stopPolling: false,
  },
  summaryDataStatus: {
    message: "Data status unknown...",
    status: "unknown",
    stopPolling: false,
  },
  paidUser: {
    paid: false,
  },
  setDisabledSidebarSteps: (disabledSidebarSteps) => {},
  setSummaryDataStatus: (dataStatus) => {},
  setDetailedDataStatus: (dataStatus) => {},
});

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  /* Initially all buttons are disabled */
  const [disabledSidebarSteps, setDisabledSidebarSteps] = useState([
    "summary_data",
    "detailed_data",
  ]);

  const [summaryDataStatus, setSummaryDataStatus] = useState({
    message: "Data status unknown...",
    status: "unknown",
    stopPolling: false,
  });
  const [detailedDataStatus, setDetailedDataStatus] = useState({
    message: "Data status unknown...",
    status: "unknown",
    stopPolling: false,
  });
  const [paidUser, setPaidUser] = useState({ paid: false });

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  function pollDataStatus(
    type: "detailed" | "summary",
    callback?: (status: any) => void
  ) {
    // If polling has finished, the callback is called.
    if (type == "detailed") {
      var url = "/api/detailed_data_status";
    } else if (type == "summary") {
      var url = "/api/summary_data_status";
    } else {
      throw new Error("Unknown type of data to query recieved.");
    }

    const setDataStatus =
      type == "summary" ? setSummaryDataStatus : setDetailedDataStatus;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        updateDisabledSidebarSteps(type, data.status, setDisabledSidebarSteps);
        setDataStatus(data);
        if (!data.stop_polling) {
          // If stopPolling is not true, poll again after 2 seconds
          setTimeout(() => pollDataStatus(type, callback), 2000);
        } else {
          if (callback) {
            callback(data.status);
          }
        }
      })
      .catch((err) => {
        console.log("oopsie, an error happened.");
      });
  }

  function updateDisabledSidebarSteps(
    type: "summary" | "detailed",
    status: string,
    setDisabledSidebarSteps: (updater: (prevSteps: string[]) => string[]) => void
  ) {
    const sidebarKey = type === "summary" ? "summary_data" : "detailed_data";

    setDisabledSidebarSteps((prevDisabledSidebarSteps: string[]) => {
      if (status === "finished" && prevDisabledSidebarSteps.includes(sidebarKey)) {
        return prevDisabledSidebarSteps.filter((item) => item !== sidebarKey);
      } else if (
        status !== "finished" &&
        !prevDisabledSidebarSteps.includes(sidebarKey)
      ) {
        return [...prevDisabledSidebarSteps, sidebarKey];
      } else {
        return prevDisabledSidebarSteps; // No changes needed
      }
    });
  }

  function getPaidStatus() {
    fetch("/api/paid")
      .then((response) => response.json())
      .then((data) => {
        setPaidUser(data);
      })
      .catch((err) => {
        console.log(
          "Oopsie, an error happened while fetching whether or not the user is paid."
        );
      });
  }

  useEffect(() => {
    getPaidStatus();
  }, []);

  useEffect(() => {
    if (summaryDataStatus.stopPolling == false) {
      pollDataStatus("summary", (status) => {
        // If we finish polling, and the status is null, the only way that can
        // happen is if we haven't ever gotten data for this user before. In
        // this case, we want to kick off data downloading, and continue
        // polling.
        if (status == null) {
          const url = "/api/refresh_summary_data";

          fetch(url)
            .then((response) => response.json())
            .then((data) => {
              if (data.refresh_accepted) {
                setSummaryDataStatus({
                  message: "Attempting to refresh data.",
                  status: "",
                  stopPolling: false,
                });
                pollDataStatus("summary");
              } else {
                setSummaryDataStatus({
                  message: data.message,
                  status: "too_recent",
                  stopPolling: true,
                });
              }
            });
        }
      });
    }
  }, [summaryDataStatus.stopPolling]);

  useEffect(() => {
    if (detailedDataStatus.stopPolling == false) {
      pollDataStatus("detailed");
    }
  }, [detailedDataStatus.stopPolling]);

  return (
    <>
      <HomeContext.Provider
        value={{
          summaryDataStatus,
          detailedDataStatus,
          paidUser,
          setDisabledSidebarSteps,
          setSummaryDataStatus,
          setDetailedDataStatus,
        }}
      >
        <TopBar sidebarVisible={sidebarVisible} toggleSidebar={toggleSidebar} />
        <div className="flex flex-row p-2 gap-2 grow overflow-auto">
          <SideBar
            sidebarVisible={sidebarVisible}
            toggleSidebar={toggleSidebar}
            disabledSidebarSteps={disabledSidebarSteps}
          />
          {/* Content */}
          <div className="bg-white rounded-lg p-2 h-full overflow-auto grow">
            {children}
          </div>
        </div>
      </HomeContext.Provider>
    </>
  );
}
