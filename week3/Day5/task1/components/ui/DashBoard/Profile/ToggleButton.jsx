"use client";
import { useState } from "react";

export default function ToggleButton({content}) {
  const [enabled, setEnabled] = useState(false);

  return (
    <div className={`h-[18.5px] w-full flex flex-row mb-[19px]`}>
        <button className={`flex ${enabled ? "justify-end" : "justify-start"} w-[36px] h-[18.5px] w-72 h-36 rounded-[98PX] transition-colors duration-300 p-[2.5px] ${enabled ? "bg-[#4FD1C5]" : "bg-[#E2E8F0]"} mr-[10px]`} 
            onClick={() => setEnabled(!enabled)}>
            <div className={`w-[13.5px] h-[13.5px] bg-white rounded-full`}></div>
        </button>
        <p className="font-normal text-xs text-[#A0AEC0]">{content}</p>
    </div>
  );
}
