export default function ProjectStatus({ status }) {
  return (
    <td className='py-[10px]'>
      <p className="font-bold text-xs">{status}</p>
    </td>
  );
}
