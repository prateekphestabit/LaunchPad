import Image from "next/image";

export default function ProjectCard({img, projectNumber, title, description}) {
    return (
        <div className="w-[370px]">
            <Image height={360} className="rounded-xl" src={img} alt={`Project ${projectNumber}`} />

            <div className="px-[9px] mt-[20px]">
                <p className="font-normal text-[10px] text-[#A0AEC0]">Project #{projectNumber}</p>
                <p className="font-bold text-lg text-[#2D3748]">{title}</p>
                <p className="font-normal text-xs text-[#A0AEC0] mt-[10.5px]">{description}</p>

                <div className="border rounded-xl border-[#4FD1C5] px-[33px] py-[8px] mt-[20px] w-fit">
                    <span className="font-bold text-[10px] text-[#4FD1C5]">VIEW ALL </span>
                </div>
            </div>
        </div>
    );
}