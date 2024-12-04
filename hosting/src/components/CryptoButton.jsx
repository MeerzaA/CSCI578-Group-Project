import React from "react";
import { useNavigate } from "react-router-dom";

const CryptoButton = (props) => {
  const navigate = useNavigate();
  const handleButtonClick = () => {
    navigate(`/${props.name}`, {
      state: { latest_sent_score: props.latest_sent_score, info: props.info },
    });
  };

  return (
    <>
      <button onClick={handleButtonClick}>{props.name}</button>
    </>
  );
};

export default CryptoButton;
