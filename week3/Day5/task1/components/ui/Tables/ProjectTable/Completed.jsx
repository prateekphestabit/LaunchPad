export default function Completed ({percent}){
  return (
    <td className='py-[10px]'>
      <p>{percent}%</p>
      <div className="w-[120px] h-[3px] rounded-full bg-[#E2E8F0]">
        <div className="h-full bg-[#4FD1C5]" 
        style={{ width: `${percent}%` }}></div>
      </div>
    </td>
  );
}
