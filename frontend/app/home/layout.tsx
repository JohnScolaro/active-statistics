"use client";

import SideBar from "@/components/side_bar/side_bar";
import TopBar from "@/components/top_bar";
import { createContext, useEffect, useState } from "react";

interface HomeContextType {
  detailedDataStatus: {
    message: string;
    status: string;
    stopPolling: boolean;
  };
  summaryDataStatus: {
    message: string;
    status: string;
    stopPolling: boolean;
  };
  paidUser: {
    paid: boolean;
  };
}

export const HomeContext = createContext<HomeContextType>({
  detailedDataStatus: {
    message: "",
    status: "",
    stopPolling: false,
  },
  summaryDataStatus: {
    message: "",
    status: "",
    stopPolling: false,
  },
  paidUser: {
    paid: false,
  },
});

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [availableSidebarSteps, setAvailableSidebarSteps] = useState([]);
  const [summaryDataStatus, setSummaryDataStatus] = useState({
    message: "",
    status: "",
    stopPolling: false,
  });
  const [detailedDataStatus, setDetailedDataStatus] = useState({
    message: "",
    status: "",
    stopPolling: false,
  });
  const [paidUser, setPaidUser] = useState({ paid: false });

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  function getDataStatus(type: string) {
    if (type == "detailed") {
      var url = "/api/detailed_data_status";
    } else if (type == "summary") {
      var url = "/api/summary_data_status";
    } else {
      throw new Error("Unknown type of data to query recieved.");
    }

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        type == "summary" ? setSummaryDataStatus(data) : setDetailedDataStatus(data);
      })
      .catch((err) => {
        console.log("oopsie, an error happened.");
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
    getDataStatus("detailed");
    getDataStatus("summary");
    getPaidStatus();
  }, []);

  return (
    <>
      <HomeContext.Provider value={{ summaryDataStatus, detailedDataStatus, paidUser }}>
        <TopBar burgerMenuFunction={toggleSidebar} />
        <div className="flex flex-row p-2 gap-2 grow overflow-auto">
          <SideBar
            sidebarVisible={sidebarVisible}
            availableSidebarSteps={availableSidebarSteps}
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
