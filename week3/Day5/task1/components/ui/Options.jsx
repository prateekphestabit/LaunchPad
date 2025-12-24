export default function Option({ optionName, iconPath, isActive, onClick, isAboveActive}) {
  let activeIconPath = iconPath;

  if (typeof iconPath === "string") {
    if (iconPath.startsWith("/w")) {
      activeIconPath = iconPath;
    } else if (iconPath.startsWith("/")) {
      activeIconPath = `/w${iconPath.slice(1)}`;
    } else {
      activeIconPath = `w${iconPath}`;
    }
  }

  const outerClass = isActive
    ? "pl-[16px] py-[12px] bg-[#FFFFFF] rounded-2xl flex items-center mb-[12px] cursor-pointer shadow-sm"
    : `pl-[16px] h-[30px] flex items-center ${
        isAboveActive ? "mb-[12px]" : "mb-[24px]"
      } cursor-pointer`;

  const iconWrapperClass = isActive
    ? "h-[30px] w-[30px] bg-[#4FD1C5] flex items-center justify-center mr-[12px] rounded-xl"
    : "h-[30px] w-[30px] bg-[#FFFFFF] flex items-center justify-center mr-[12px] rounded-xl shadow-sm";

  return (
    <div onClick={onClick} className={outerClass}>
      
      <div className={iconWrapperClass}>
        <img
          className="h-[15px] w-[15px]"
          src={isActive ? activeIconPath : iconPath}
          alt=""
        />
      </div>

      <span
        className={
          isActive
            ? "font-sans font-bold text-[#2D3748] text-xs"
            : "font-sans font-bold text-[#A0AEC0] text-xs"
        }
      >
        {optionName}
      </span>
    </div>
  );
}