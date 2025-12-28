import Navbar              from '@/../components/ui/Navbar.jsx';
import Sidebar             from '@/../components/ui/Sidebar.jsx';
import Card                from '@/../components/ui/DashBoard/Card.jsx';
import PurityDashboardCard from '@/../components/ui/DashBoard/PurityDashboardCard.jsx';
import RocketsBannerCard   from '../../../components/ui/DashBoard/RocketsBannerCard.jsx';
import ActiveUsersGraph    from '../../../components/ui/DashBoard/ActiveUsersGraph.jsx';
import SalesOverviewCard   from '../../../components/ui/DashBoard/SalesOverviewCard.jsx';

export const metadata = {
  title: 'Dashboard Page',
  description: 'Main dashboard page with overview cards and graphs',
}

export default function DashboardPage() {
  return (
    <div className="flex flex-row bg-[#f8f9fa] h-full">
      <Sidebar />
      <div className="flex flex-col p-[33.5px] w-full">
        <Navbar pageTitle={'Dashboard'}/>
        
        <div className='mr-[22px] mt-[29px] w-full h-[80px] flex gap-[24px]'>
          <Card title={`Today's Money`} value={`$53,000`} delta={`+55%`} icon={`wallet.svg`} color={false}/>
          <Card title={`Today's Users`} value={`2,300`} delta={`+5%`} icon={`globe.svg`} color = {false}/>
          <Card title={`New Client's`} value={`+3,052`} delta={`-14%`} icon={`file.svg`} color = {true}/>
          <Card title={`Total Sales`} value={`$173,000`} delta={`+8%`} icon={`cart.svg`} color = {false}/>
        </div>

        <div className="mr-[22px] mt-[23.5px] w-full h-[291px] flex gap-[24px]">
          <PurityDashboardCard />
          <RocketsBannerCard />
        </div>

        <div className="mr-[22px] mt-[23.5px] w-full flex gap-[24px]">
          <ActiveUsersGraph />
          <SalesOverviewCard />
        </div>
      </div>
    </div>
  );
}