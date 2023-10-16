import React, { useState } from "react";
import { useEffect } from "react";
import { Collapse } from "@mui/material";
import { ExpandLess } from "@mui/icons-material";
import { CenteredSpinner } from "../spinner/spinner";
import Link from "next/link";
import styles from "./side_bar.module.css";
import { usePathname } from "next/navigation";

interface SideBarProps {
  sidebarVisible: boolean;
}

export default function SideBar(props: SideBarProps) {
  return (
    <div
      className={`w-72 h-full overflow-auto shrink-0 p-2 rounded-lg bg-green-500 ${
        props.sidebarVisible ? `absolute z-10 ${styles.custom_sidebar}` : "hidden"
      } lg:block`}
    >
      <SideBarButtons />
    </div>
  );
}

function SideBarButtons() {
  // Sidebar data state
  const [menuData, setMenuData] = useState([]);

  useEffect(() => {
    fetch("/api/tabs")
      .then((response) => response.json())
      .then((data) => setMenuData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Create the download_strava_data tab manually here.
  const download_strava_data_step = (
    <MenuItem
      item={{
        key: "download_strava_data",
        name: "Download Strava Data",
        type: "xxx",
        items: [],
      }} // Replace with your fixed data
      key="download_strava_data"
      indentation={0}
    />
  );

  if (menuData.length == 0) {
    return <CenteredSpinner />;
  } else {
    const otherMenuItems = menuData.map((item: Item) => (
      <MenuItem item={item} key={item.key} indentation={0} />
    ));
    const menuItems = [download_strava_data_step, ...otherMenuItems];
    return menuItems;
  }
}

interface Item {
  key: string;
  name: string;
  type: string;
  items: Item[];
}

interface MenuItemProps {
  item: Item;
  indentation: number;
}

const MenuItem = ({ item, indentation }: MenuItemProps) => {
  const Component = hasChildren(item) ? SideBarMultiLevelButton : SideBarButton;
  return <Component item={item} indentation={indentation} />;
};

function hasChildren(item: Item) {
  return item.items.length != 0;
}

const SideBarButton = ({ item, indentation }: { item: Item; indentation: number }) => {
  const link_url = `/home/${item.key}`;
  const pathname = usePathname();
  const backgroundStyle = pathname == link_url ? "bg-green-300" : "bg-green-400";

  return (
    <Link href={`/home/${item.key}`}>
      <div className={`p-2 mb-2 rounded-lg ${backgroundStyle} hover:bg-green-300`}>
        <SideBarButtonText text={item.name} indentation={indentation} />
      </div>
    </Link>
  );
};

const SideBarMultiLevelButton = ({
  item,
  indentation,
}: {
  item: Item;
  indentation: number;
}) => {
  const items = item.items;
  const [open, setOpen] = useState(false);

  const handleClick = () => {
    setOpen((prev) => !prev);
  };

  const iconStyle = {
    transform: `rotate(${open ? 0 : 180}deg)`,
    transition: "transform 0.2s ease",
  };

  return (
    <>
      <div
        className="flex flex-row p-2 mb-2 rounded-lg bg-green-400 hover:bg-green-600"
        onClick={handleClick}
      >
        <SideBarButtonText text={item.name} indentation={0} />
        <ExpandLess style={iconStyle} />
      </div>
      <Collapse in={open} timeout="auto" unmountOnExit>
        {items.map((item) => (
          <MenuItem item={item} key={item.key} indentation={indentation + 1} />
        ))}
      </Collapse>
    </>
  );
};

function SideBarButtonText({ text, indentation }: { text: string; indentation: number }) {
  const marginLeft = `${indentation}em`;
  return (
    <div className="grow" style={{ marginLeft }}>
      {text}
    </div>
  );
}
