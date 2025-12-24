export default function Status({status}) {
    const text = status ? 'Online' : 'Offline';
    return (
        <td className='py-[10px]'>
            <div className={`w-fit px-[10.5] py-[2.5px] rounded-lg ${status ? 'bg-[#48BB78]' : 'bg-[#CBD5E0]'}`}>
                <p className={`font-bold text-xs text-white`}>{text}</p>
            </div>
        </td>
    );
}
