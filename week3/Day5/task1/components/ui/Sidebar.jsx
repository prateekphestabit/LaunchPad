"use client";

import { useState } from "react";
import Option from "./Options.jsx";
import Image from "next/image.js";
import bg from '@/../public/background.svg';

export default function Sidebar({currPage = "Dashboard"}) {

    
  const mainOptions = [
    { key: "dashboard", optionName: "Dashboard", iconPath: "/dashboard.svg" },
    { key: "tables", optionName: "Tables", iconPath: "/chart.svg" },
    { key: "billing", optionName: "Billing", iconPath: "/billing.svg" },
    { key: "rtl", optionName: "RTL", iconPath: "/rtl.svg" },
  ];

  const accountOptions = [
    { key: "about", optionName: "About Us", iconPath: "/profile.svg" },
    { key: "profile", optionName: "Profile", iconPath: "/profile.svg" },
    { key: "signIn", optionName: "Sign In", iconPath: "/signIn.svg" },
    { key: "signUp", optionName: "Sign Up", iconPath: "/signUp.svg" },
  ];

  const [activeOptionName, setActiveOptionName] = useState(currPage);

  const renderOptions = (opts) =>
    opts.map((opt, idx) => {
      const isActive = activeOptionName === opt.optionName;
      const isAboveActive = activeOptionName === opts[idx + 1]?.optionName;

      return (
        <Option
          key={opt.key}
          optionName={opt.optionName}
          iconPath={opt.iconPath}
          isActive={isActive}
          isAboveActive={isAboveActive}
          onClick={() => {
            setActiveOptionName(opt.optionName);
            if     (opt.key === "about")     window.location.href = "/about";
            else if(opt.key === "profile")   window.location.href = "/dashboard/profile";
            else if(opt.key === "dashboard") window.location.href = "/dashboard";
            else if(opt.key === "tables")    window.location.href = "/tables";
            else if(opt.key === "signIn")   window.location.href = "/login";
          }}
        />
      );
    });

  return (
    <aside className="font-sans w-[246.5px] h-[780.5px] mt-[44px] ml-[17px] flex flex-col items-center"> 
      
      <div className="font-sans flex flex-row justify-center items-center h-[21px] mb-[27.5px] font-semibold text-sm">
        <img className="h-[22px] w-[22px] mr-[12px]" src="/logo.svg" alt="logo" />
        PURITY UI DASHBOARD
      </div>

      <div className="w-[233px] mb-[22.5] h-[2px] bg-gradient-to-r from-transparent via-gray-200 via-gray-300 via-gray-200 to-transparent "></div>

      
      <div className="w-[219.5px] h-[408px]">
        {renderOptions(mainOptions)}

        <span className="block font-bold text-xs ml-[16px] mb-[24px]">ACCOUNT PAGES</span>

        {renderOptions(accountOptions)}
      </div>

      <div className="mt-[69.5px] w-[246.5px] h-[465px] flex flex-col">
        <Image width={246.5} height={465} src={bg} alt="" />
      </div>
    </aside>
  );
}


