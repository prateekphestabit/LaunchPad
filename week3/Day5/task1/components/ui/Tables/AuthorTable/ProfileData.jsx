import Image from "next/image";

export default function ProfileData({ img, name, email }) {
  return (
    <td className='flex flex-row items-center py-[10px]'>
        <Image src={img} alt={name} width={40} height={40} className='rounded-xl' />
        <div className='ml-2'>
            <p className='font-bold text-xs text-[#2D3748]'>{name}</p>
            <p className='font-normal text-xs text-[#718096]'>{email}</p>
        </div>
    </td>
  );
}
