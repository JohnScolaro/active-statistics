import React, { useState } from "react";
import { useEffect } from "react";
import { Collapse } from "@mui/material";
import { ExpandLess } from "@mui/icons-material";
import { CenteredSpinner } from "../spinner/spinner";
import Link from "next/link";
import styles from "./side_bar.module.css";
import { usePathname, useRouter } from "next/navigation";
import { wrappedFetch } from "../../lib/fetch";

interface SideBarProps {
  sidebarVisible: boolean;
  toggleSidebar: () => void;
  disabledSidebarSteps: string[];
}

export default function SideBar(props: SideBarProps) {
  return (
    <>
      {/* This magic div is secretly behind the sidebar when it's open (when
        the screen is small) and closes the bar when people click on it. */}
      <div
        className={`overflow-auto shrink-0 p-2 z-30 ${props.sidebarVisible
          ? `absolute z-40 ${styles.custom_behind_sidebar} lg:static`
          : "hidden"
          } lg:hidden`}
        onClick={props.toggleSidebar}
      ></div>
      {/* This is the actual sidebar */}
      <div
        className={`w-72 h-full overflow-auto shrink-0 p-2 rounded-lg bg-green-500 absolute z-40 lg:block transition-all lg:static ${styles.custom_sidebar
          } ${props.sidebarVisible ? "" : "translate-x-[-300px] lg:translate-x-0"} `}
      >
        <SideBarButtons disabledSidebarSteps={props.disabledSidebarSteps} />
      </div>
    </>
  );
}

interface SidebarButtonsProps {
  disabledSidebarSteps: string[];
}

function SideBarButtons(props: SidebarButtonsProps) {
  // Sidebar data state
  const [menuData, setMenuData] = useState([]);
  const router = useRouter();

  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    wrappedFetch(
      `${apiBaseUrl}/api/tabs`,
      (data) => setMenuData(data),
      (error) => console.error("Error fetching tabs: ", error),
      router
    );
  }, [apiBaseUrl, router]);

  // Create the download_strava_data tab manually here.
  const download_strava_data_step = (
    <MenuItem
      item={{
        key: "",
        name: "Download Strava Data",
        type: "",
        items: [],
      }} // Replace with your fixed data
      key="download_strava_data"
      indentation={0}
      disabled={false}
    />
  );

  if (menuData.length == 0) {
    return <CenteredSpinner />;
  } else {
    const otherMenuItems = menuData.map((item: Item) => (
      <MenuItem
        item={item}
        key={item.key}
        indentation={0}
        disabled={props.disabledSidebarSteps.includes(item.key)}
      />
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
  disabled: boolean;
}

const MenuItem = ({ item, indentation, disabled }: MenuItemProps) => {
  const ButtonOrMultiButton = hasChildren(item) ? SideBarMultiLevelButton : SideBarButton;
  return (
    <ButtonOrMultiButton item={item} indentation={indentation} disabled={disabled} />
  );
};

function hasChildren(item: Item) {
  return item.items.length != 0;
}

interface ButtonOrMultiButtonProps {
  item: Item;
  indentation: number;
  disabled: boolean;
}

const SideBarButton = ({ item, indentation, disabled }: ButtonOrMultiButtonProps) => {
  const link_url = `/home/${item.key}`;
  const pathname = usePathname();

  const enabledBgStyle =
    pathname == link_url ? "bg-green-300" : "bg-green-400 hover:bg-green-300";
  const disabledBgStyle = "bg-gray-400 text-gray-600";

  if (disabled) {
    return (
      <div
        className={`p-2 mb-2 rounded-lg flex ${disabled ? disabledBgStyle : enabledBgStyle
          } `}
      >
        <SideBarButtonText text={item.name} indentation={indentation} />
        🚫
      </div>
    );
  } else {
    return (
      <Link href={`/home/${item.key}`}>
        <div
          className={`p-2 mb-2 rounded-lg flex ${disabled ? disabledBgStyle : enabledBgStyle
            } `}
        >
          <SideBarButtonText text={item.name} indentation={indentation} />
        </div>
      </Link>
    );
  }
};

const SideBarMultiLevelButton = ({
  item,
  indentation,
  disabled,
}: ButtonOrMultiButtonProps) => {
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
        className={`flex flex-row p-2 mb-2 rounded-lg ${disabled ? "bg-gray-400 text-gray-600" : "bg-green-400 hover:bg-green-600"
          }`}
        onClick={handleClick}
      >
        <SideBarButtonText text={item.name} indentation={indentation} />
        <ExpandLess style={iconStyle} />
      </div>
      <Collapse in={open} timeout="auto" unmountOnExit>
        {items.map((item) => (
          <MenuItem
            item={item}
            key={item.key}
            indentation={indentation + 1}
            disabled={disabled}
          />
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
