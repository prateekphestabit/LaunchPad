import Image from "next/image";
import graph from '@/../public/Graph.svg';
import Stats from "@/../components/ui/Stats.jsx";
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

      <div className="flex flex-row">
        <Stats icon={wallet} label="Users" value="32,984" />
        <Stats icon={wsignUp} label="Clicks" value="2,42m" />
        <Stats icon={cart} label="Sales" value="2,400$" />
        <Stats icon={wrtl} label="Items" value="320" />
      </div>
    </div>
  );
}