export default function Card({ title, value, delta, icon, color }) {
    const Color = color ? 'text-[#E53E3E]' : 'text-[#48BB78]';

    return (
    <div className="flex items-center justify-between rounded-2xl bg-white w-[382px] h-[80px] pl-[21.5px] pr-[17.5px] shadow-sm">
      <div className="w[107px] h-[44px]">
        <p className="text-xs font-bold text-[#A0AEC0]">{title}</p>

        <div className="flex items-baseline">
          <p className="text-lg font-bold text-[#2D3748]">
            {value}
          </p>

          <span className="w-[5px]"></span>

          <p className={`text-sm font-bold ${Color}`}>{delta}</p>
        </div>
      </div>

      <div className="grid h-[45px] w-[45px] place-items-center rounded-xl bg-[#4FD1C5]">
        <img className="h-[22.5px] w-[22.5px]" src={icon} alt="" />
      </div>
    </div>
  );
}
