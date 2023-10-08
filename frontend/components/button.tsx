import React, { MouseEvent } from 'react';

interface ButtonProps {
    text: string;
    onClick: (event: MouseEvent<HTMLButtonElement>) => void;
}

const Button: React.FC<ButtonProps> = ({ text, onClick }) => {
    return (
        <button onClick={onClick}>
            {text}
        </button>
    );
}

export default Button;
