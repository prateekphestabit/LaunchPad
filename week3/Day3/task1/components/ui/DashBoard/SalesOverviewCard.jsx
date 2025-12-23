import SalesGraph from '@/../public/SalesGraph.svg';
import Image from 'next/image';

export default function SalesOverviewCard() {
  return (
    <div className="bg-white rounded-2xl p-[16px] shadow-sm w-fit h-full">
        <div className="mt-[24px]">
            <p className="text-[#2D3748] font-bold text-lg">Sales Overview</p>
            <p className="font-normal text-[#A0AEC0] text-sm"><span className="text-green-500 font-bold text-sm">(+5) more</span> in 2026</p>

            <Image src={SalesGraph} alt="Sales Graph" className='mt-[41px]'/>
        </div>
    </div>
  );
}