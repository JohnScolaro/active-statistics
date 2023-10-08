import React, { ReactNode } from 'react';

interface MultiButtonProps {
    children: ReactNode;
}

const MultiButton: React.FC<MultiButtonProps> = ({ children }) => {
    return (
        <div>
            <div>Multibutton context</div>
            {children}
        </div>
    );
}

export default MultiButton;
