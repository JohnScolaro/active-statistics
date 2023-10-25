interface Data {
  [key: string]: string[];
}

export default function ImagePage({ data }: { data: Data }) {
  console.log(data);
  return (
    <>
      <div className="flex flex-col gap-2">
        {Object.keys(data).map((key: string, index: number) => (
          <div key={index} className="p-2 border-2 border-green-500 rounded-lg">
            <div className="flex justify-center">
              <img
                src={data[key][0]}
                alt="Image"
                className="h-auto w-auto max-h-[780px]"
              />
            </div>
            <div className="text-center text-sm">{data[key][1]}</div>
          </div>
        ))}
      </div>
    </>
  );
}
