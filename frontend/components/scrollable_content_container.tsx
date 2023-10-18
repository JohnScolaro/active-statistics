import React, { ReactNode } from "react";

interface ScrollableContentContainerProps {
  children: ReactNode;
  modalState: boolean;
}

export default function ScrollableContentContainer({
  children,
  modalState,
}: ScrollableContentContainerProps) {
  return (
    <div className={"bg-white p-2 m-2 rounded-lg flex flex-col gap-4 overflow-auto"}>
      {children}
    </div>
  );
}
