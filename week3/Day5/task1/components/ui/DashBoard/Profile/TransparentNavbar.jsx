"use client";

import { useState } from "react";
import Image from "next/image.js";
import ProfileButton from "./ProfileButton.jsx";


export default function ProfileCard({dp, name, email, options, children, rounded=true, center=false}) {

    const [activeOptionName, setActiveOptionName] = useState('SIGN IN');
    const onClick = (optionName) => {
        if(optionName === 'DASHBOARD') window.location.href = "/dashboard";
        else if(optionName === 'PROFILE') window.location.href = "/dashboard/profile";
        setActiveOptionName(optionName);
    }
    
    return (
        <div className={`bg-[#ffffffd0] rounded-2xl w-full  flex justify-between items-center pl-[16.5px] pr-[28.5px] shadow-md ${center ? "absolute left-1/2 -translate-x-1/2  max-w-[1500px] h-[80px] top-[24px]" : "h-[113px]"}`}>
            <div className="h-[85px] w-fit flex flex-row items-center">
                <Image className={`${rounded ? "rounded-xl h-[80px] w-[80px]" : "h-[30px] w-[30px]"}`} src={dp} alt="" />
                <div className="ml-[22px]">
                    <div className="font-bold text-lg text-[#2D3748]">{name}</div>
                    <p className="font-normal text-sm text-[#718096]">{email}</p>
                </div>
            </div>
            <div className="h-[35px] flex flex-row gap-[1px]">
                {options.map((opt, index) =>  <ProfileButton key={index} id={index} optionName={opt.name} ActiveOptionName={activeOptionName} icon={opt.icon}  onClick={onClick} />)}
            </div>
            {children}
        </div>
    );
}