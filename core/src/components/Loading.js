import React from "react";
import loading from "../assets/loading.svg";

const Loading = () => (
  <div className="spinner">
    <img src={loading} alt="Loading" style={{width: "60px"}}/>
  </div>
);

export default Loading;
