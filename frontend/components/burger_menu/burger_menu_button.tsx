import styles from "./burger_menu_button.module.css";

interface BurgerMenuIconProps {
  isBurgerIcon: boolean;
  toggleIcon: () => void;
}

export default function BurgerMenuIcon(props: BurgerMenuIconProps) {
  const buttonClasses = props.isBurgerIcon
    ? styles.burger_menu_button
    : `${styles.burger_menu_button} ${styles.active}`;

  return (
    <div className={buttonClasses} onClick={props.toggleIcon}>
      <span></span>
    </div>
  );
}
