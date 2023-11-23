interface ImageData {
  url: string;
  caption: string;
}

export default function ImagePage({ data }: { data: ImageData[] }) {
  return (
    <>
      <div className="flex flex-col gap-2">
        {data.map((image, index) => (
          <div key={index} className="p-2 border-2 border-green-500 rounded-lg">
            <div className="flex justify-center">
              <img src={image.url} alt="Image" className="h-auto w-auto max-h-[780px]" />
            </div>
            <div className="text-center text-sm">{image.caption}</div>
          </div>
        ))}
      </div>
    </>
  );
}
