import React from 'react';

interface SideMenuProps {
    isOpen: boolean;
    onClose: () => void;
}

function SideMenu({ isOpen, onClose }: SideMenuProps) {
    const menuStyle = {
        width: isOpen ? '250px' : '0',
    };

    return (
        <div className="side-menu" style={menuStyle}>
            <button className="close-button" onClick={onClose}>
                &times;
            </button>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
        </div>
    );
}

export default SideMenu;
