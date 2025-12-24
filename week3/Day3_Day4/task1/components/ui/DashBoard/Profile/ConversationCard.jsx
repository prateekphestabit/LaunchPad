import Image from "next/image"; 

export default function ConversationCard({img, name, msg}) {
    return (
        <div className="h-[50px] flex flex-row justify-between items-center mb-[21px]">
            <div className="flex flex-row">
                <Image src={img} width={50} height={50} className="rounded-xl" alt="chat" />
                <div className="ml-[15px]">
                    <p className="font-bold text-sm text-[#2D3748]">{name}</p>
                    <p className="font-normal text-sm text-[#718096]">{msg}</p>
                </div>
            </div>

            <p className="font-bold text-[10px] text-[#4FD1C5]">REPLY</p>
        </div>
    );
}