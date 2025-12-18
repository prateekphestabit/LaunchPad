export default function Option({optionName, iconPath, isActive, }) {

    if(!isActive){
        return (
            <div className="pl-[16px] h-[30px]  flex items-center mb-[24px]">
                <div className="h-[30px] w-[30px] bg-[#FFFFFF] flex items-center justify-center mr-[12px] rounded-xl">
                    <img className="h-[15px] w-[15px]" src={iconPath} alt="" />
                </div>

                <span className="font-sans font-bold text-[#A0AEC0] text-xs">{optionName}</span>
            </div>
        );
    }
}