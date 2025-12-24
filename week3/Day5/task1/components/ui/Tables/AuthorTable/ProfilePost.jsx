export default function ProfilePost({ post, subPost }) {
  return (
    <td className='py-[10px]'>
        <p className='font-bold text-xs text-[#2D3748]'>{post}</p>
        <p className='font-normal text-xs text-[#718096]'>{subPost}</p>
    </td>
  );
}
