"use client";

import { useState } from "react";
import Option from "./Options.jsx";

export default function Sidebar() {
  const mainOptions = [
    { key: "dashboard", optionName: "Dashboard", iconPath: "/dashboard.svg" },
    { key: "tables", optionName: "Tables", iconPath: "/chart.svg" },
    { key: "billing", optionName: "Billing", iconPath: "/billing.svg" },
    { key: "rtl", optionName: "RTL", iconPath: "/rtl.svg" },
  ];

  const accountOptions = [
    { key: "profile", optionName: "Profile", iconPath: "/profile.svg" },
    { key: "signIn", optionName: "Sign In", iconPath: "/signIn.svg" },
    { key: "signUp", optionName: "Sign Up", iconPath: "/signUp.svg" },
  ];

  // One shared state => selection syncs across BOTH sections
  const [activeOptionName, setActiveOptionName] = useState(null);

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
          onClick={() => setActiveOptionName(opt.optionName)}
          isAboveActive={isAboveActive}
        />
      );
    });

  return (
    <aside className="bg-[#f8f9fa] font-sans w-[246.5px] h-[780.5px] mt-[44px] ml-[17px] flex flex-col items-center">
      {/* logo and title */}
      <div className="font-sans flex flex-row justify-center items-center h-[21px] mb-[27.5px] font-semibold text-sm">
        <img className="h-[22px] w-[22px] mr-[12px]" src="/logo.svg" alt="logo" />
        PURITY UI DASHBOARD
      </div>

      {/* dividing line  */}
      <div className="w-[233px] mb-[22.5] h-[2px] bg-gradient-to-r from-transparent via-gray-200 via-gray-300 via-gray-200 to-transparent "></div>

      
      <div className="w-[219.5px] h-[408px]">
        {/* options */}
        {renderOptions(mainOptions)}

        {/* Account Pages */}
        <span className="block font-bold text-xs ml-[16px] mb-[24px]">ACCOUNT PAGES</span>

        {/* New options below Account Pages */}
        {renderOptions(accountOptions)}
      </div>

      <div className="mt-[69.5px] w-[246.5px] h-[465px] flex flex-col">
          <img className="mr-[17px] ml-[17px]" src="./background.svg" alt="" />
      </div>
    </aside>
  );
}
