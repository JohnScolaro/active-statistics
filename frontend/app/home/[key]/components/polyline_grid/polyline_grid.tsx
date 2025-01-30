import { useEffect, useRef, useState } from "react";
import Select from "react-select";
import polyline from "@mapbox/polyline";

interface ImageData {
  polyline: string;
  start_datetime: string; // Format: "YYYY-MM-DDTHH:mm:ss"
  type: string;
}

export default function PolylineGridPage({ data }: { data: ImageData[] }) {
  const [filteredYear, setFilteredYear] = useState<string | "All">("All");

  // Extract unique years from the data
  const years = Array.from(
    new Set(data.map((activity) => new Date(activity.start_datetime).getFullYear().toString()))
  ).sort();
  const yearOptions = [{ value: "All", label: "All" }, ...years.map((year) => ({ value: year, label: year }))];

  const filteredData =
    filteredYear === "All"
      ? data
      : data.filter(
        (activity) => new Date(activity.start_datetime).getFullYear().toString() === filteredYear
      );

  const groupedData = groupByType(filteredData);

  return (
    <div className="flex flex-col gap-4">
      {/* Year Filter */}
      <div className="flex items-center gap-2 mb-4">
        <label className="text-lg font-semibold">Year:</label>
        <Select
          options={yearOptions}
          value={yearOptions.find((option) => option.value === filteredYear)}
          onChange={(option) => setFilteredYear(option?.value || "All")}
          className=""
          styles={{
            control: (provided) => ({
              ...provided,
              border: "2px solid #22c55e", // Tailwind green-500 color
              borderRadius: "0.5rem", // Rounded corners
              boxShadow: "none",
            }),
            option: (provided, state) => ({
              ...provided,
              backgroundColor: state.isFocused ? "#86efac" : "white", // Tailwind green-200 on hover
              color: "black",
            }),
          }}
          placeholder="Select a year"
        />
      </div>

      {/* Activity Grid */}
      {Object.entries(groupedData).map(([type, activities], index) => (
        <div key={index} className="p-2 border-2 border-green-500 rounded-lg flex flex-col gap-2">
          <CanvasGrid polylines={activities.map((a) => a.polyline)} activityType={type} />
        </div>
      ))}
    </div>
  );
}

function groupByType(data: ImageData[]): Record<string, ImageData[]> {
  return data.reduce((acc, item) => {
    if (!acc[item.type]) {
      acc[item.type] = [];
    }
    acc[item.type].push(item);
    return acc;
  }, {} as Record<string, ImageData[]>);
}

function decodePolyline(encoded: string): [number, number][] {
  return polyline.decode(encoded);
}

function applyEquirectangularApproximation(polyline: [number, number][]): [number, number][] {
  const R = 6371; // Earth radius in km
  const referenceLat = polyline[0][0];
  return polyline.map(([lat, lon]) => {
    const x = (R * lon * Math.PI) / 180 * Math.cos((referenceLat * Math.PI) / 180);
    const y = (R * lat * Math.PI) / 180;
    return [x, y];
  });
}

function customScalePolyline(polyline: [number, number][]): [number, number][] {
  const minX = Math.min(...polyline.map(([x]) => x));
  const minY = Math.min(...polyline.map(([, y]) => y));
  const maxX = Math.max(...polyline.map(([x]) => x));
  const maxY = Math.max(...polyline.map(([, y]) => y));

  const width = maxX - minX;
  const height = maxY - minY;
  if (width === 0 || height === 0) return [];

  const scalingFactor = 1 / Math.max(width, height);
  return polyline.map(([x, y]) => [(x - minX) * scalingFactor, (maxY - y) * scalingFactor]);
}

function CanvasGrid({ polylines, activityType }: { polylines: string[]; activityType: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Disable antialiasing for sharp rendering
    ctx.imageSmoothingEnabled = false;

    const decodedPolylines = polylines.map(decodePolyline);
    const processedPolylines = decodedPolylines.map((polyline) =>
      customScalePolyline(applyEquirectangularApproximation(polyline))
    );

    const gridSize = Math.ceil(Math.sqrt(processedPolylines.length));
    const borderSizePx = 6;

    const canvasHeight = 1000;
    const canvasWidth = canvasHeight; // Keep the canvas square
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    const squareSize = (canvas.width - (gridSize + 1) * borderSizePx) / gridSize;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    processedPolylines.forEach((polyline, index) => {
      const col = index % gridSize;
      const row = Math.floor(index / gridSize);

      const startX = col * squareSize + (col + 1) * borderSizePx;
      const startY = row * squareSize + (row + 1) * borderSizePx;

      ctx.beginPath();
      polyline.forEach(([x, y], i) => {
        const canvasX = startX + x * squareSize;
        const canvasY = startY + y * squareSize;
        if (i === 0) {
          ctx.moveTo(canvasX, canvasY);
        } else {
          ctx.lineTo(canvasX, canvasY);
        }
      });
      ctx.lineWidth = 1;
      ctx.strokeStyle = "black";
      ctx.stroke();
    });
  }, [polylines]);

  const handleDownload = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const image = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.href = image;
    link.download = "grid.png";
    link.click();
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <canvas ref={canvasRef} className="border rounded h-full max-h-[80vh] max-w-full" />
      <div className="text-sm text-center">Activity type: {activityType}</div>
      <button
        onClick={handleDownload}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
      >
        Download Image
      </button>
    </div>
  );
}
