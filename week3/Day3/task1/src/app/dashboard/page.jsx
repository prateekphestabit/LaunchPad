import Navbar from '../../../components/ui/Navbar.jsx';
import Sidebar from '../../../components/ui/Sidebar.jsx';
import Card from '../../../components/ui/Card.jsx';
import PurityDashboardCard from '../../../components/ui/PurityDashboardCard.jsx';
import RocketsBannerCard from '../../../components/ui/RocketsBannerCard.jsx';

export default function DashboardPage() {
  return (
    <div className="flex flex-row">
      <Sidebar />
      <div className="flex flex-col p-[33.5px]">
        <Navbar pageTitle={'Dashboard'}/>
        <div className='mr-[22px] mt-[29px] w-[1600px] h-[80px] flex justify-between'>
          <Card title={`Today's Money`} value={`$53,000`} delta={`+55%`} icon={`wallet.svg`} color={false}/>
          <Card title={`Today's Users`} value={`2,300`} delta={`+5%`} icon={`globe.svg`} color = {false}/>
          <Card title={`New Client's`} value={`+3,052`} delta={`-14%`} icon={`file.svg`} color = {true}/>
          <Card title={`Total Sales`} value={`$173,000`} delta={`+8%`} icon={`cart.svg`} color = {false}/>
        </div>

        <div className="mr-[22px] mt-[23.5px] w-[1600px] h-[291px] flex justify-between">
          <PurityDashboardCard />
          <RocketsBannerCard />
        </div>
      </div>
    </div>
  );
}