import styles from "./spinner.module.css";

export function Spinner() {
  return (
    <div className={styles.lds_ellipsis}>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  );
}

export function CenteredSpinner() {
  return (
    <div className="flex h-full flex-col justify-center">
      <div className="flex flex-row justify-center">
        <Spinner />
      </div>
    </div>
  );
}
