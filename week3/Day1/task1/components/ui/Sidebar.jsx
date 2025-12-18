import Option from './Options.jsx';

export default function Sidebar() {
  return (
    <aside className="bg-amber-300 font-sans w-[246.5px] h-[1015.5px] mt-[44px] ml-[17px] flex flex-col items-center">
      
      {/* logo and title */}
      <div className="flex flex-row justify-center items-center h-[21px] mb-[27.5px] font-semibold text-sm">
        <img className="h-[22px] w-[22px] mr-[12px]" src="/logo.svg" alt="logo" />
        PURITY UI DASHBOARD
      </div>



      {/* dividing line  */}
      <div className="w-[233px] mb-[22.5] h-px bg-gradient-to-r from-transparent via-gray-200 via-gray-300 via-gray-200 to-transparent "></div>



      {/* options   */}
      <div className="bg-yellow-900 w-[219.5px] h-[408px]">
        <Option optionName={"Dashboard"} iconPath={"/dashboard.svg"} isActive={false} />
        <Option optionName={"Tables"} iconPath={"/chart.svg"} isActive={false} />
        <Option optionName={"Billing"} iconPath={"/billing.svg"} isActive={false} />
        <Option optionName={"RTL"} iconPath={"/rtl.svg"} isActive={false} />
      </div>
    </aside>
    );
}
