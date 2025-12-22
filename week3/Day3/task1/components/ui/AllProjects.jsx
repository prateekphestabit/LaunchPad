import ProjectCard from "@/../components/ui/ProjectCard.jsx";
import project1 from '@/../public/project1.svg';
import project2 from '@/../public/project2.svg';
import project3 from '@/../public/project3.svg';

export default function AllProjects(){
    return (
        <div className="rounded-2xl shadow-sm px-[22px] pt-[26px] mt-[24px] pb-[28px]">
            <p className="font-bold text-lg text-[#2D3748] mb-[6px]">Projects</p>
            <p className='font-bold text-[10px] text-[#A0AEC0] mb-[25.5px]'>Architects design houses</p>

            <div className="flex flex-row gap-[24px]">
                <ProjectCard 
                    img={project1} 
                    projectNumber={1} 
                    title="Modern" 
                    description="As Uber works through a huge amount of internal management turmoil." 
                />
                <ProjectCard 
                    img={project2} 
                    projectNumber={2} 
                    title="Scandinavian" 
                    description="Music is something that every person has his or her own specific opinion about." 
                />
                <ProjectCard 
                    img={project3} 
                    projectNumber={3} 
                    title="Minimalist" 
                    description="As Uber works through a Different people have different taste, and various types of music. amount of internal management turmoil." 
                />

                <div className="flex flex-col justify-center items-center w-[370px] h-[353px] border border-[#E0E1E2] rounded-xl">
                    <div className="font-bold text-lg text-[#718096]">+</div>
                    <div className="font-bold text-lg text-[#718096]">Create a New Project</div>
                </div>
            </div>
        </div>
    );
}