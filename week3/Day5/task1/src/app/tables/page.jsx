import Navbar        from '@/../components/ui/Navbar.jsx';
import Sidebar       from '@/../components/ui/Sidebar.jsx';
import TableCard     from '@/../components/ui/Tables/TablesCard.jsx';
import Table         from '@/../components/ui/Tables/Table.jsx';
import ProfileData   from '@/../components/ui/Tables/AuthorTable/ProfileData.jsx';
import ProfilePost   from '@/../components/ui/Tables/AuthorTable/ProfilePost.jsx';
import Status        from '@/../components/ui/Tables/AuthorTable/Status.jsx';
import Employed      from '@/../components/ui/Tables/AuthorTable/Employed.jsx';
import Edit          from '@/../components/ui/Tables/AuthorTable/Edit.jsx';
import dp1           from '@/../public/dp1.svg';
import dp5           from '@/../public/dp5.svg';
import dp6           from '@/../public/dp6.svg';
import dp7           from '@/../public/dp7.svg';
import dp8           from '@/../public/dp8.svg';
import dp9           from '@/../public/dp9.svg';
import xd            from '@/../public/xd.svg';
import A             from '@/../public/A.svg';
import BA            from '@/../public/BA.svg';
import spotify       from '@/../public/spotify.svg';
import box           from '@/../public/box.svg';
import ProjectStatus from '@/../components/ui/Tables/ProjectTable/ProjectStatus.jsx';
import completed     from '@/../components/ui/Tables/ProjectTable/Completed.jsx';
import Completed     from '@/../components/ui/Tables/ProjectTable/Completed.jsx';
import More          from '@/../components/ui/Tables/ProjectTable/More.jsx';


export default function DashboardPage() {

  const authorTableData = {
    head: ['AUTHOR', 'FUNCTION', 'STATUS', 'EMPLOYED', ' '],
    body: [
      [
        <ProfileData img={dp1} name={'Esthera Jackson'} email={'esthera@simmmple.com'} />,
        <ProfilePost post={'Manager'} subPost={'Organization'} />,
        <Status status={true} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
      [
        <ProfileData img={dp5} name={'Alexa Liras'} email={'alexa@simmmple.com'} />,
        <ProfilePost post={'Programmer'} subPost={'Developer'} />,
        <Status status={false} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
      [
        <ProfileData img={dp6} name={'Laurent Michael'} email={'laurent@simmmple.com'} />,
        <ProfilePost post={'Executive'} subPost={'Projects'} />,
        <Status status={true} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
      [
        <ProfileData img={dp7} name={'Freduardo Hill'} email={'freduardo@simmmple.com'} />,
        <ProfilePost post={'Manager'} subPost={'Organization'} />,
        <Status status={true} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
      [
        <ProfileData img={dp8} name={'Daniel Thomas'} email={'daniel@simmmple.com'} />,
        <ProfilePost post={'Programmer'} subPost={'Developer'} />,
        <Status status={false} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
      [
        <ProfileData img={dp9} name={'Mark Wilson'} email={'mark@simmmple.com'} />,
        <ProfilePost post={'Designer'} subPost={'UI/UX Design'} />,
        <Status status={false} />,
        <Employed empId={'14/06/21'} />,
        <Edit />
      ],
    ]
    
  };

  const projectTableData = {
    head: ['COMPANIES', 'BUDGET', 'STATUS', 'COMPLETION', ' '],
    body: [
      [
        <ProfileData img={xd} name={'Chakra Soft UI Version'} email={' '} />,
        <ProfilePost post={'$14,000'} subPost={' '} />,
        <ProjectStatus status={'Working'} />,
        <Completed percent={60} />,
        <More />
      ],
      [
        <ProfileData img={A} name={'Chakra Soft UI Version'} email={' '} />,
        <ProfilePost post={'$3,000'} subPost={' '} />,
        <ProjectStatus status={'Canceled'} />,
        <Completed percent={10} />,
        <More />
      ],[
        <ProfileData img={BA} name={'Chakra Soft UI Version'} email={' '} />,
        <ProfilePost post={'Not set'} subPost={' '} />,
        <ProjectStatus status={'Done'} />,
        <Completed percent={100} />,
        <More />
      ],[
        <ProfileData img={spotify} name={'Chakra Soft UI Version'} email={' '} />,
        <ProfilePost post={'$32,000'} subPost={' '} />,
        <ProjectStatus status={'Done'} />,
        <Completed percent={100} />,
        <More />
      ],[
        <ProfileData img={box} name={'Chakra Soft UI Version'} email={' '} />,
        <ProfilePost post={'$400'} subPost={' '} />,
        <ProjectStatus status={'Working'} />,
        <Completed percent={25} />,
        <More />
      ],
      
    ]
  };

  return (
    <div className="flex flex-row bg-[#f8f9fa] h-full">
      <Sidebar currPage = 'Tables'/>
      <div className="flex flex-col w-full pl-[33.5px] pr-[22px] pt-[22.5px]">
        <Navbar pageTitle={'tables'} pl={16.5} pr={22.5}/>

        <TableCard title={'Authors Table'}>
          <Table data={authorTableData}/>
        </TableCard>        

        <TableCard title={'Projects'}>

          <Table data={projectTableData}/>
        </TableCard>
      </div>
    </div>
  );
}