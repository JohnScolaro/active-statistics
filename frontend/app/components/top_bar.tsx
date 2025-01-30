import Link from "next/link";
import Image from "next/image";
import BurgerMenuIcon from "./burger_menu/burger_menu_button";

interface TopBarProps {
  sidebarVisible: boolean;
  toggleSidebar: () => void;
}

export default function TopBar({ sidebarVisible, toggleSidebar }: TopBarProps) {
  return (
    <div className="bg-green-600 flex justify-between p-2 mt-2 ml-2 mr-2 rounded-lg h-14 max-h-14">
      <div className="lg:hidden">
        <BurgerMenuIcon isBurgerIcon={!sidebarVisible} toggleIcon={toggleSidebar} />
      </div>
      <Link href="/" className="text-white text-2xl font-bold">
        <span className="align-middle">Active Statistics</span>
      </Link>
      <Link href="https://github.com/JohnScolaro/active-statistics" className="h-full">
        <Image
          src="/github-mark-white.svg"
          width={0}
          height={0}
          alt="GitHub Logo"
          className="h-full w-auto"
        />
      </Link>
    </div>
  );
}
