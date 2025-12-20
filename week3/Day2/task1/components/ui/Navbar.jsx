export default function Navbar() {
  return (
    <nav className="mt-[22.5px] w-[1558px] h-[52px] flex justify-between mr-[47.5px] ml-[14.5px]">
      <div>
        <div>
            <span className="font-sans text-[#A0AEC0] text-xs font-normal">Pages</span>
            <span className="font-sans text-black text-xs font-normal">  / </span>
            <span className="font-sans text-black text-xs font-normal">Tables</span>
        </div>
        <div>
            <span className="font-bold font-sans text-black text-sm">Tables</span>
        </div>
      </div>

      <div className="flex items-center">
        <div className="flex items-center gap-3 px-4 py-3 rounded-full border border-gray-200 bg-white mr-[18px]">
            <img src="./search.svg" alt="" />

            <input type="text" placeholder="Type here..."
            className="w-full text-sm text-gray-700 placeholder-gray-400 outline-none bg-transparent"
            />
        </div>

        <div className="flex mr-[19px]">
            <img className="h-[12px] w-[12px] mr-[4px]" src="./person.svg" alt="" />
            <span className="text-xs font-bold">Sign In</span>
        </div>

        <img className="h-[12px] w-[12px] mr-[17px]" src="./settings.svg" alt="" />
        
        <img className="h-[12px] w-[12px]" src="./bell.svg" alt="" />
      </div>
    </nav>
  );
}