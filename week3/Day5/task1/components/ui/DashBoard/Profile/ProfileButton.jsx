import Image from "next/image";

export default function ProfileButton({optionName, ActiveOptionName, icon, onClick}) {

    let buttonStyle = optionName === ActiveOptionName ? "bg-white shadow-md rounded-xl" : "bg-transparent";
    return (
        <div className={`w-[135px] h-[35px] flex flex-row items-center justify-center gap-[2px] ${buttonStyle}`} onClick={() => onClick(optionName)}>
            <Image className="w-[11px] h-[11px]" src={icon} alt={optionName} />
            <p className="font-bold text-[10px] text-[#2D3748]">{optionName}</p>
        </div>
    );
}