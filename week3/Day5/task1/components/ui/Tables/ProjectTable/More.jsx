import more from '@/../public/more.svg';    
import Image from 'next/image';

export default function More() {   
    return (
        <td><Image src={more} alt="More" width={20} height={20}/></td>
    );
}