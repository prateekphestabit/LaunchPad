"use client";

import { useState } from "react";
import Image from "next/image.js";
import ProfileButton from "./ProfileButton.jsx";
import overview from "@/../public/overview.svg";
import teams from "@/../public/teams.svg";
import projects from "@/../public/projects.svg";

export default function ProfileCard({dp, name, email}) {

    const [activeOptionName, setActiveOptionName] = useState('OVERVIEW');
    const onClick = (optionName) => setActiveOptionName(optionName);
    
    return (
        <div className="bg-[#fffffff3] rounded-2xl w-full h-[113px] flex justify-between items-center pl-[16.5px] pr-[28.5px] shadow-md">
            <div className="h-[85px] w-[258px] flex flex-row items-center">
                <Image className="h-[80px] w-[80px] rounded-xl" src={dp} alt="" />
                <div className="ml-[22px]">
                    <p className="font-bold text-lg text-[#2D3748]">{name}</p>
                    <p className="font-normal text-sm text-[#718096]">{email}</p>
                </div>
            </div>
            <div className="h-[35px] flex flex-row">
                <ProfileButton optionName="OVERVIEW" ActiveOptionName={activeOptionName} icon={overview}  onClick={onClick} />
                <ProfileButton optionName="TEAMS" ActiveOptionName={activeOptionName} icon={teams}  onClick={onClick} />
                <ProfileButton optionName="PROJECTS" ActiveOptionName={activeOptionName} icon={projects}  onClick={onClick} />
            </div>
        </div>
    );
}