import ToggleButton from "@/../components/ui/DashBoard/Profile/ToggleButton.jsx";


export default function LoginForm(){

    return (
        <div className="w-fit h-fit">
            <p className="font-bold text-4xl text-[#4FD1C5]">Welcome Back</p>
            <p className="font-bold text-sm text-[#A0AEC0] mt-[9px]">Enter your email and password to sign in</p>
            <form action="" className="flex flex-col">
                
                <label htmlFor="email" className="font-normal text-sm text-[#2D3748] mt-[36px]">Email</label>
                <input 
                    type="email" 
                    placeholder="Your email address" 
                    required 
                    className="border border-[#E2E8F0] rounded-xl pl-[20px] py-[15px] pr-[210px] mt-[5px]"
                />

                <label htmlFor="password" className="font-normal text-sm text-[#2D3748] mt-[24px]">Password</label>
                <input 
                    type="password" 
                    placeholder="Your password" 
                    required 
                    className="border border-[#E2E8F0] rounded-xl pl-[20px] py-[15px] pr-[210px] mt-[5px]"
                />

                <div className="flex flex-row pt-[24px]">
                    <ToggleButton /> <p className="font-normal text-xs text-[#2D3748]">Remember me</p>
                </div>

                <button type="submit" className="bg-[#4FD1C5] text-white text-[10px] font-bold rounded-xl py-[12px] mt-[36px]">Sign In</button>
                
                <div className="flex justify-center mt-[22px]">
                    <p className="font-normal text-sm text-[#A0AEC0]">Don't have an account? <span className="text-[#4FD1C5] font-semibold">Sign up</span></p>
                </div>
            </form>
        </div>
    );
}