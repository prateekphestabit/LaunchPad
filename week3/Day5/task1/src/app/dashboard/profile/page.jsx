import Sidebar from '@/../components/ui/Sidebar.jsx';
import Navbar from '@/../components/ui/Navbar';
import ProfileCard from '../../../../components/ui/DashBoard/Profile/ProfileCard.jsx';
import AllProfileInfo from '../../../../components/ui/DashBoard/Profile/AllProfileInfo.jsx';
import AllProjects from '../../../../components/ui/DashBoard/Profile/AllProjects.jsx';

import dp from '@/../public/dp1.svg';

export const metadata = {
  title: 'Profile Page',
  description: 'User profile page with settings, project and personal information.',
}

export default function ProfilePage() {

  let name = "Esthera Jackson";
  let email = "esthera@simmmple.com";

  return (
    <div className="flex flex-row w-full bg-[#f8f9fa]">
        <Sidebar currPage='Profile'/>
        
        <div className='w-full  flex flex-col pr-[24px] pt-[24px] pl-[33.5px] '>
          <div className='bg-[#4FD1C5] rounded-2xl flex flex-row h-[300px] w-full '>
            <div className="w-full h-full rounded-2xl bg-[url('@/../public/profileBackground.svg')] bg-no-repeat bg-cover bg-center pr-[23.5px] pl-[14.5px] pt-[22.5px] ">
              <Navbar pageTitle={'Profile'} color={true}/>
            </div>  
          </div>
          
          
          <div className='relative w-full -top-[65px] px-[24px]'><ProfileCard dp={dp} name={name} email={email}/></div>
          
          <AllProfileInfo />
          <AllProjects/>
        </div>
    </div>
  );
}