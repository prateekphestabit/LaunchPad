import Image from "next/image.js";
import graph from '@/../public/Graph.svg';
import Stats from "./Stats.jsx";
import wallet from "@/../public/wallet.svg";
import wsignUp from "@/../public/wsignUp.svg";
import cart from "@/../public/cart.svg";
import wrtl from "@/../public/wrtl.svg";

export default function ActiveUsersGraph() {
  return (
    <div className="bg-white rounded-2xl p-[16px] shadow-sm w-fit">
      <Image src={graph} alt="Active Users Graph" width={620} height={222}/>

      <div className="mt-[24px]">
        <p className="text-[#2D3748] font-bold text-lg">Active Users</p>
        <p className="font-normal text-[#A0AEC0] text-sm"><span className="text-green-500 font-bold text-sm">(+23)</span> than last week</p>
      </div>

      <div className="flex flex-row justify-between pr-[40px]">
        <Stats icon={wallet} label="Users" value="32,984" percentage="50" />
        <Stats icon={wsignUp} label="Clicks" value="2,42m" percentage="30" />
        <Stats icon={cart} label="Sales" value="2,400$" percentage="90" />
        <Stats icon={wrtl} label="Items" value="320" percentage="70" />
      </div>
    </div>
  );
}