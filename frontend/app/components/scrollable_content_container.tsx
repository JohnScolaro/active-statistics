import React, { ReactNode } from "react";

interface ScrollableContentContainerProps {
  children: ReactNode;
}

export default function ScrollableContentContainer({
  children,
}: ScrollableContentContainerProps) {
  return (
    <div className={"bg-white p-2 m-2 rounded-lg flex flex-col gap-4 overflow-auto"}>
      {children}
    </div>
  );
}
