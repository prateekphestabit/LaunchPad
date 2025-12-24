export default function TablesCard({ title, children }) {
    return (
        <div className="bg-white rounded-2xl shadow-md p-[23.5px] mt-[25px]">
            <p className="text-lg font-bold text-lg text-[#2D3748]">{title}</p>
            {children}
        </div>
    );
}
