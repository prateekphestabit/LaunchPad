import person from '@/../public/person.svg';
import wperson from '@/../public/wprofile.svg';
import settings from '@/../public/settings.svg';
import wsettings from '@/../public/wsettings.svg';
import bell from '@/../public/bell.svg';
import wbell from '@/../public/wbell.svg';
import search from '@/../public/search.svg';

import Image from 'next/image';

export default function Navbar({pageTitle, color = false}) {
  let color1 = color ? 'text-white' : 'text-[#A0AEC0]';
  let color2 = color ? 'text-white' : 'text-black';

  let personIcon = color ? wperson : person;
  let settingsIcon = color ? wsettings : settings;
  let bellIcon = color ? wbell : bell;

  return (
    <nav className="w-full h-[52px] flex justify-between">
      <div>
        <div>
            <span className={`font-sans ${color1} text-xs font-normal`}>Pages</span>
            <span className={`font-sans ${color2} text-xs font-normal`}>  / </span>
            <span className={`font-sans ${color2} text-xs font-normal`}>{pageTitle}</span>
        </div>
        <div>
            <span className={`font-bold font-sans ${color2} text-sm`}>{pageTitle}</span>
        </div>
      </div>

      <div className="flex items-center">
        <div className="flex items-center gap-3 px-4 py-3 rounded-2xl border border-gray-200 bg-white mr-[18px]">
            <Image src={search} alt="search" />

            <input type="text" placeholder="Type here..."
            className="w-full text-sm text-gray-700 placeholder-gray-400 outline-none bg-transparent"
            />
        </div>

        <div className="flex mr-[19px]">
            <Image className="h-[12px] w-[12px] mr-[4px]" src={personIcon} alt="person" />
            <span className={`text-xs font-bold ${color2}`}>Sign In</span>
        </div>

        <Image className="h-[12px] w-[12px] mr-[17px]" src={settingsIcon} alt="settings" />

        <Image className="h-[12px] w-[12px]" src={bellIcon} alt="bell" />
      </div>
    </nav>
  );
}