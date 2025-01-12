import * as React from "react";
import { LocationSelector } from "../location/LocationSelector";
import { NavigationLink } from "./navigationLink";
import { navigationLinks } from "./navigationData";

export function NavigationBar() {
  return (
    <div className="flex flex-wrap gap-10 py-4 pr-20 pl-3 bg-white border-solid border-b-[0.667px] border-b-gray-200 max-md:pr-5">
      <LocationSelector />
      <div className="flex overflow-hidden overflow-x-auto gap-10 justify-center items-center py-2.5 pr-1.5 my-auto text-sm leading-5 text-center whitespace-nowrap min-h-[40px] text-neutral-600">
        {navigationLinks.map((link) => (
          <NavigationLink key={link.id} text={link.text} />
        ))}
      </div>
      <div className="flex overflow-hidden flex-col justify-center rounded min-h-[52px]">
        <img
          loading="lazy"
          src="https://cdn.builder.io/api/v1/image/assets/TEMP/2948ab2927cfa800ee682974a8607cd653490a17ce640dde6333dbc4b3b17bed?placeholderIfAbsent=true&apiKey=614886db34c5450aaa8841fb26b8c531"
          className="object-contain flex-1 aspect-[7.81] w-[405px]"
          alt=""
        />
      </div>
    </div>
  );
}