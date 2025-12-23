export default function ProfileInfoCard({title, children}){
  return (
    <div className="flex-1 h-[377.5] bg-white rounded-2xl shadow-sm px-[22px] pt-[26px]">
        <p className="font-bold text-lg text-[#2D3748] mb-[17px]">{title}</p>
        {children}
    </div>
  );  
} 