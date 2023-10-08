import React, { ReactNode } from 'react';
import MultiButton from './multi-button';
import Button from './button';

interface SidebarProps {
    buttons: ReactNode[];
    multiButtons: ReactNode[];
}

const Sidebar: React.FC<SidebarProps> = ({ buttons, multiButtons }) => {
    return (
        <div className="sidebar">
            {multiButtons.map((multiButton, index) => (
                <MultiButton key={`multi-button-${index}`}>
                    {multiButton}
                </MultiButton>
            ))}
            {buttons.map((button, index) => {
                // Check if button has valid props before spreading
                if (React.isValidElement(button) && button.props) {
                    return (
                        <Button key={`button-${index}`} {...button.props} />
                    );
                }
                return null; // Handle invalid or null button.props
            })}
        </div>
    );
}

export default Sidebar;
