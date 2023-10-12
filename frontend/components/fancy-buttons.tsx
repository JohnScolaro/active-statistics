import React, { useState } from "react";
import { useEffect } from "react";
import { List, Collapse, ListItemButton } from "@mui/material";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import { CenteredSpinner } from "./spinner";
import Link from "next/link";

export default function SideBarButtons() {
    // State to hold the retrieved menu data
    const [menuData, setMenuData] = useState([]);

    useEffect(() => {
        fetch('/api/tabs')
            .then((response) => response.json())
            .then((data) => setMenuData(data))
            .catch((error) => console.error('Error fetching data:', error));
    }, []);

    if (menuData.length == 0) {
        return <CenteredSpinner />
    } else {
        return menuData.map((item, key) => <MenuItem key={key} item={item} />);
    }
}

const MenuItem = ({ item }) => {
    const Component = hasChildren(item) ? MultiLevel : SingleLevel;
    return <Component item={item} />;
};

const SingleLevel = ({ item }) => {
    return (
        <Link href='/home/boogers'>
            <ListItemButton disableGutters={true} disableRipple={true} disableTouchRipple={true} sx={list_item_button_style}>
                <div>{item.name}</div>
            </ListItemButton >
        </Link>
    );
};

const MultiLevel = ({ item }) => {
    const { items: children } = item;
    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen((prev) => !prev);
    };

    return (
        <>
            <ListItemButton disableGutters={true} disableRipple={true} disableTouchRipple={true} sx={list_item_group_style} onClick={handleClick}>
                <div className="grow">{item.name}</div>
                {open ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Collapse in={open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding={true}>
                    {children.map((child, key) => (
                        <MenuItem key={key} item={child} />
                    ))}
                </List>
            </Collapse>
        </>
    );
};


function hasChildren(item) {
    const { items: children } = item;

    if (children === undefined) {
        return false;
    }

    if (children.constructor !== Array) {
        return false;
    }

    if (children.length === 0) {
        return false;
    }

    return true;
}

const list_item_button_style = {
    'backgroundColor': 'rgb(74 222 128)',
    'padding': '0.5rem',
    'border-radius': '0.5rem',
    '&:hover': {
        'backgroundColor': 'rgb(21 128 61)'
    },
    'marginBottom': '0.5rem',
};

const list_item_group_style = {
    'backgroundColor': 'rgb(74 222 128)',
    'padding': '0.5rem',
    'border-radius': '0.5rem',
    '&:hover': {
        'backgroundColor': 'rgb(21 128 61)'
    },
    'marginBottom': '0.5rem',
}


// bg-green-50 ->   rgb(240 253 244);
// bg-green-100 ->  rgb(220 252 231);
// bg-green-200 ->  rgb(187 247 208);
// bg-green-300 ->  rgb(134 239 172);
// bg-green-400 ->  rgb(74 222 128);
// bg-green-500 ->  rgb(34 197 94);
// bg-green-600 ->  rgb(22 163 74);
// bg-green-700 ->  rgb(21 128 61);
// bg-green-800 ->  rgb(22 101 52);
// bg-green-900 ->  rgb(20 83 45);
// bg-green-950 ->  rgb(5 46 22);
