import React, { useState } from "react";
import { useEffect } from "react";
import { Collapse } from "@mui/material";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import { CenteredSpinner } from "./spinner";
import Link from "next/link";

export default function SideBarButtons() {
    // State to hold the retrieved menu data
    const [menuData, setMenuData] = useState([]);
    const [selectedButtonKey, setSelectedButtonKey] = useState('');

    useEffect(() => {
        fetch('/api/tabs')
            .then((response) => response.json())
            .then((data) => setMenuData(data))
            .catch((error) => console.error('Error fetching data:', error));
    }, []);

    const handleButtonClick = (key: string) => {
        setSelectedButtonKey(key);
    };

    if (menuData.length == 0) {
        return <CenteredSpinner />
    } else {
        return menuData.map((item: Item) => <MenuItem item={item} key={item.key} indentation={0} selectedButtonKey={selectedButtonKey} setThisButtonSelected={handleButtonClick} />);
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
    selectedButtonKey: string;
    setThisButtonSelected: (key: string) => void;
}

const MenuItem = ({ item, indentation, selectedButtonKey, setThisButtonSelected }: MenuItemProps) => {
    const Component = hasChildren(item) ? SideBarMultiLevelButton : SideBarButton;
    return <Component item={item} indentation={indentation} selectedButtonKey={selectedButtonKey} setThisButtonSelected={setThisButtonSelected} />;
};


function hasChildren(item: Item) {
    return (item.items.length != 0);
}

const SideBarButton = ({ item, indentation, selectedButtonKey, setThisButtonSelected }: { item: Item, indentation: number, selectedButtonKey: string, setThisButtonSelected: (key: string) => void }) => {
    const isSelected = selectedButtonKey === item.key;
    const backgroundStyle = isSelected ? 'bg-green-300' : 'bg-green-400';


    return (
        <Link href={`/home/${item.key}`} onClick={() => { setThisButtonSelected(item.key) }}>
            <div className={`p-2 mb-2 rounded-lg ${backgroundStyle} hover:bg-green-300`}>
                <SideBarButtonText text={item.name} indentation={indentation} />
            </div>
        </Link>
    );
};

const SideBarMultiLevelButton = ({ item, indentation, selectedButtonKey, setThisButtonSelected }: { item: Item, indentation: number, selectedButtonKey: string, setThisButtonSelected: (key: string) => void }) => {
    const items = item.items;
    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen((prev) => !prev);
    };

    const iconStyle = {
        transform: `rotate(${open ? 0 : 180}deg)`,
        transition: 'transform 0.2s ease',
    };

    return (
        <>
            <div className="flex flex-row p-2 mb-2 rounded-lg bg-green-400 hover:bg-green-600" onClick={handleClick}>
                <SideBarButtonText text={item.name} indentation={0} />
                <ExpandLess style={iconStyle} />
            </div>
            <Collapse in={open} timeout="auto" unmountOnExit>
                {items.map((item) => (
                    <MenuItem item={item} key={item.key} indentation={indentation + 1} selectedButtonKey={selectedButtonKey} setThisButtonSelected={setThisButtonSelected} />
                ))}
            </Collapse>
        </>
    );
};

function SideBarButtonText({ text, indentation }: { text: string, indentation: number }) {
    const marginLeft = `${indentation}em`;
    return <div className="grow" style={{ marginLeft }}>{text}</div>;
}
