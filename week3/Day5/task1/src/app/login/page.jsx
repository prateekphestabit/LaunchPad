import ProfileCard from "../../../components/ui/DashBoard/Profile/TransparentNavbar";
import overview from "@/../public/overview.svg";
import bprofile from "@/../public/bprofile.svg";
import bsignUp from '@/../public/bsignUp.svg';
import bkey from '@/../public/bkey.svg';
import logo from '@/../public/logo.svg';
import LoginForm from "@/../components/ui/Login/form.jsx";

export default function LoginPage(){
    const options = [
        { name: "DASHBOARD", icon: overview },
        { name: "PROFILE", icon: bprofile },
        { name: "SIGN UP", icon: bsignUp },
        { name: "SIGN IN", icon: bkey}
    ];
    return (
        <div className="bg-white w-screen h-screen flex flex-row relative">
            <div className="bg-white flex-7">
                <ProfileCard dp={logo} name={"PURITY UI DASHBOARD"} options={options} rounded={false} center={true}> 
                    <div className="bg-[#151928] font-bold text-[10px] text-white px-[34px] py-[10px] rounded-2xl">
                        Free Download
                    </div>    
                </ProfileCard>

                <div className="w-full h-full flex flex-row justify-center items-center">
                    <LoginForm />
                </div>
            </div>
            <div className="bg-[url('@/../public/chakraImg.svg')] bg-no-repeat bg-cover bg-center flex-5 h-[80vh] rounded-bl-2xl"></div>
        </div>
    );
}