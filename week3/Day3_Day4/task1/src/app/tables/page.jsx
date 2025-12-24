import Navbar              from '@/../components/ui/Navbar.jsx';
import Sidebar             from '@/../components/ui/Sidebar.jsx';

export default function DashboardPage() {
  return (
    <div className="flex flex-row bg-[#f8f9fa] h-full">
      <Sidebar currPage='tables'/>
      <div className="flex flex-col p-[33.5px] w-full">
        <Navbar pageTitle={'Tables'}/>
        
        
      </div>
    </div>
  );
}