"use client";

import "../globals.css";
import { useRouter } from "next/navigation";
import { getCookie } from "cookies-next";
import { useEffect, useState, useContext, createContext } from "react";
import { CenteredSpinner } from "./spinner/spinner";

interface LoggedInContextInterface {
  loggedIn: boolean;
  setLoggedIn: (value: boolean) => void;
}

// Create the context and provide initial values
const LoggedInContext = createContext<LoggedInContextInterface>({
  loggedIn: false,
  setLoggedIn: () => {},
});

export function useLoggedIn() {
  return useContext(LoggedInContext);
}

export default function Base({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Check if there is a "logged_in" cookie.
    const isLoggedIn = getCookie("logged_in") == "true";
    setLoggedIn(isLoggedIn);
    setLoading(false); // Set loading to false after checking the cookie
  }, []);

  useEffect(() => {
    if (!loading) {
      if (!loggedIn) {
        router.push("/");
      }
    }
  }, [loading, loggedIn, router]);

  if (loading) {
    // Render a loading indicator or any content you prefer while checking the cookie.
    return <CenteredSpinner />;
  }

  return (
    <LoggedInContext.Provider value={{ loggedIn: loggedIn, setLoggedIn: setLoggedIn }}>
      <div className="flex flex-col bg-green-100 h-screen">{children}</div>
    </LoggedInContext.Provider>
  );
}
