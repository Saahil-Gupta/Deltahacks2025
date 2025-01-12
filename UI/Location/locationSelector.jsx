import * as React from "react";

export function LocationSelector() {
  return (
    <div 
      className="flex relative items-center self-start px-4 py-3 text-2xl font-medium leading-none text-center text-black rounded-lg border border-solid border-neutral-200 min-h-[50px]"
      role="button"
      tabIndex={0}
    >
      <img
        loading="lazy"
        src="https://cdn.builder.io/api/v1/image/assets/TEMP/fb6219086bdb4bde6723f8b0a3b3467abee2332dd8357717bf3d5c644b2d4a0f?placeholderIfAbsent=true&apiKey=614886db34c5450aaa8841fb26b8c531"
        className="object-contain z-0 shrink-0 self-stretch my-auto aspect-square w-[29px]"
        alt=""
      />
      <div className="flex z-0 shrink-0 self-stretch my-auto w-2 h-2" />
      <div className="z-0 self-stretch my-auto w-[225px]">Hamilton, ON</div>
      <div className="flex z-0 shrink-0 self-stretch my-auto w-4 h-2" />
      <img
        loading="lazy"
        src="https://cdn.builder.io/api/v1/image/assets/TEMP/c66333b525a3bc3572375e5973269790ab829058aaea43fc7841c4c0ac5f2754?placeholderIfAbsent=true&apiKey=614886db34c5450aaa8841fb26b8c531"
        className="object-contain absolute right-3 inset-y-3.5 z-0 shrink-0 self-start w-5 aspect-[0.91] left-[303px]"
        alt=""
      />
    </div>
  );
}