export default function PurityDashboardCard() {
  return (
    <div className="basis-3/5 h-[290px] bg-white rounded-2xl p-[17.5px] flex justify-between shadow-sm">
      <div className="w-[330px] h-[256px]">
        <p className="text-bold text-xs mb-2 text-[#A0AEC0]">Built by developers</p>

        <h2 className="text-lg font-bold text-[#2D3748] mb-2">
          Purity UI Dashboard
        </h2>

        <p className="font-normal text-sm text-[#A0AEC0] mb-4">
          From colors, cards, typography to complex elements, you will find the full
          documentation.
        </p>

        <div className="h-[111px]" />

        <p className="text-xs font-semibold font-[#2D3748] inline-flex items-center">
          Read More -&gt;
        </p>
      </div>

      <div className="w-[360px] h-[256px]">
        <img className="rounded-2xl" src="./imagee.svg" alt="" />
      </div>
    </div>
  );
}