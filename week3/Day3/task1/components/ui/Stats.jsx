import Image from "next/image";

export default function Stats({icon, label, value}) {
    return (
        <div className="mt-[36.5px] mr-[90px] ml-[10px]">
            <div className="flex flex-row">
                <div className="bg-[#4FD1C5] rounded-md w-[25px] h-[25px] flex justify-center items-center">
                    <Image src={icon} alt={label} width={12.5} height={12.5} />
                </div>
                <p className="ml-[10px] text-bold text-xs text-[#A0AEC0]" >{label}</p>
            </div>

            <p className="font-bold text-lg text-[#2D3748]">{value}</p>
        </div>
    );
}