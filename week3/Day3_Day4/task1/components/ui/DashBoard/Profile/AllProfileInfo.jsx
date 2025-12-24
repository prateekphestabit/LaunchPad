import ToggleButton from "./ToggleButton.jsx";
import ProfileInfoCard from '@/../components/ui/DashBoard/Profile/ProfileInfoCard.jsx';
import facebookIcon from '@/../public/facebook.svg';
import twitterIcon from '@/../public/twitter.svg';
import instagramIcon from '@/../public/instagram.svg';
import ConversationCard from "./ConversationCard.jsx";
import Image from "next/image.js";
import dp1 from '@/../public/dp1.svg';
import dp2 from '@/../public/dp2.svg';
import dp3 from '@/../public/dp3.svg';
import dp4 from '@/../public/dp4.svg';


export default function AllProfileInfo(){
    return (
        <div className='flex flex-row gap-[24px] w-full'>
            <ProfileInfoCard title={'Platform Settings'}> 
                <p className='font-bold text-[10px] text-[#A0AEC0] mb-[20px]'>ACCOUNT</p>
                <ToggleButton content={'Email me when someone follows me'} />
                <ToggleButton content={'Email me when someone answers on my post'} />
                <ToggleButton content={'Email me when someone mentions me'} />

                <div className='h-[7px]'></div>

                <p className='font-bold text-[10px] text-[#A0AEC0] mb-[20px]'>APPLICATION</p>

                <ToggleButton content={'New launches and projects'} />
                <ToggleButton content={'Monthly product updates'} />
                <ToggleButton content={'Subscribe to newsletter'} />
            </ProfileInfoCard>

            <ProfileInfoCard title={'Profile Information'}>
                <p className='font-normal text-xs text-[#A0AEC0] mb-[60px]'>
                    Hi, I’m Alec Thompson, Decisions: If you can’t decide, the answer is no. If two equally 
                    difficult paths, choose the one more painful in the short term (pain avoidance is 
                    creating an illusion of equality).
                </p>

                <div className="flex flex-row h-[18px] mb-[15px]">
                    <p className="font-bold text-xs text-[#718096]">Full Name:</p>
                    <p className="font-normal text-xs text-[#A0AEC0] ml-[10px]">Alec M. Thompson</p>
                </div>
                
                <div className="flex flex-row h-[18px] mb-[15px]">
                    <p className="font-bold text-xs text-[#718096]">Mobile:</p>
                    <p className="font-normal text-xs text-[#A0AEC0] ml-[10px]">(44) 123 1234 123</p>
                </div>

                <div className="flex flex-row h-[18px] mb-[15px]">
                    <p className="font-bold text-xs text-[#718096]">Email:</p>
                    <p className="font-normal text-xs text-[#A0AEC0] ml-[10px]">alecthompson@mail.com</p>
                </div>
                        
                <div className="flex flex-row h-[18px] mb-[15px]">
                    <p className="font-bold text-xs text-[#718096]">Location:</p>
                    <p className="font-normal text-xs text-[#A0AEC0] ml-[10px]">United States</p>
                </div>

                <div className="flex flex-row h-[18px] mb-[15px]">
                    <p className="font-bold text-xs text-[#718096]">Social Media:</p>
                    <Image src={facebookIcon} alt="Facebook" width={12} height={12} className="ml-[14px]" />
                    <Image src={twitterIcon} alt="Twitter" width={12} height={12} className="ml-[14px]" />
                    <Image src={instagramIcon} alt="Instagram" width={12} height={12} className="ml-[14px]" />
                </div>
            </ProfileInfoCard>


            <ProfileInfoCard title={'Conversations'}>
                <div className="w-full">
                    <ConversationCard img={dp1} name={'Esthera Jackson'} msg={'Hi! I need more informations...'} />
                    <ConversationCard img={dp2} name={'Esthera Jackson'} msg={'Awesome work, can you change...'} />
                    <ConversationCard img={dp3} name={'Esthera Jackson'} msg={'Have a great afternoon...'} />
                    <ConversationCard img={dp4} name={'Esthera Jackson'} msg={'About files I can...'} />
                </div>
            </ProfileInfoCard>
        </div>
    );_
} 