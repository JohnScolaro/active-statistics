'use client'

import { useState } from 'react';
import styles from './burger-menu-button.module.css'

interface BurgerMenuIconProps {
    onButtonClick: () => void;
}

export default function BurgerMenuIcon(props: BurgerMenuIconProps) {
    const [isActive, setIsActive] = useState(false);

    const menuBtnFunction = () => {
        setIsActive(!isActive);
        props.onButtonClick();
    };
    const buttonClasses = isActive
        ? `${styles.burger_menu_button} ${styles.active}`
        : styles.burger_menu_button;

    return (
        <div className={buttonClasses} onClick={menuBtnFunction}>
            <span></span>
        </div>
    );
}
