import Image from "next/image";

export default function Stats({icon, label, value, percentage}) {

    let barWidth = percentage + '%';
    return (
        <div className="mt-[36.5px] w-[102px] mb-[10px] flex flex-col gap-[4px]">
            <div className="flex flex-row items-center">
                <div className="bg-[#4FD1C5] rounded-md w-[25px] h-[25px] flex justify-center items-center">
                    <Image src={icon} alt={label} width={12.5} height={12.5} />
                </div>
                <p className="ml-[10px] text-bold text-xs text-[#A0AEC0]" >{label}</p>
            </div>

            <p className="font-bold text-lg text-[#2D3748]">{value}</p>

            <div className="w-full h-[4px] bg-[#E2E8F0] rounded-full">
                <div 
                className="h-full bg-[#4FD1C5] rounded-full"
                style={{ width: `${barWidth}` }}
            />
            </div>
        </div>
    );
}