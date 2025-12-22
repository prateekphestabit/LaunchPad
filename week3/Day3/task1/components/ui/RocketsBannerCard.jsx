export default function RocketsBannerCard() {
  return (
    <div className="basis-2/5 h-[290px] bg-white rounded-2xl shadow-sm relative overflow-hidden p-[17.5px]">
      <div className="w-full h-full rounded-xl bg-[url('/rocketImg.svg')] bg-no-repeat bg-cover bg-center pt-[20px] pl-[21px] pb-[13px]">
        <div className="w-[400px] h-[222px]">
          <p className="font-bold text-lg text-white">Work with the Rockets</p>

          <p className="font-normal text-sm text-white">
            Wealth creation is an evolutionarily recent positive-sum game.
          </p>

          <p className="font-normal text-sm text-white">
            It is all about who take the opportunity first.
          </p>

          <div className="h-[129.5px]" />

          <p className="text-xs font-semibold text-white inline-flex items-center">
            Read More -&gt;
          </p>
        </div>
      </div>
    </div>
  );
}