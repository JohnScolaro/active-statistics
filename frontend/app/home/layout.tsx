"use client";

import SideBar from "@/components/side_bar/side_bar";
import TopBar from "@/components/top_bar";
import { useState } from "react";

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  // Sidebar visible state
  const [sidebarVisible, setSidebarVisible] = useState(false);

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <>
      <TopBar burgerMenuFunction={toggleSidebar} />
      <div className="flex flex-row p-2 gap-2 grow overflow-auto">
        <SideBar sidebarVisible={sidebarVisible} />
        {/* Content */}
        <div className="bg-white rounded-lg p-2 h-full overflow-auto grow">
          {children}
        </div>
      </div>
    </>
  );
}
