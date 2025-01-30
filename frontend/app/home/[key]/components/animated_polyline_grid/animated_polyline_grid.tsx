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
    const [animationTime, setAnimationTime] = useState<number>(5000); // Default to 5 seconds

    // Extract unique years from the data
    const years = Array.from(
        new Set(data.map((activity) => new Date(activity.start_datetime).getFullYear().toString()))
    ).sort();
    const yearOptions = [{ value: "All", label: "All" }, ...years.map((year) => ({ value: year, label: year }))];

    const animationOptions = [
        { value: 1000, label: "1 second" },
        { value: 5000, label: "5 seconds" },
        { value: 10000, label: "10 seconds" },
    ];

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
            <div className="flex items-center gap-2">
                <label className="text-sm md:text-lg font-semibold">Year:</label>
                <Select
                    options={yearOptions}
                    value={yearOptions.find((option) => option.value === filteredYear)}
                    onChange={(option) => setFilteredYear(option?.value || "All")}
                    className=""
                    styles={{
                        control: (provided) => ({
                            ...provided,
                            border: "2px solid #22c55e",
                            borderRadius: "0.5rem",
                            boxShadow: "none",
                        }),
                        option: (provided, state) => ({
                            ...provided,
                            backgroundColor: state.isFocused ? "#86efac" : "white",
                            color: "black",
                        }),
                    }}
                    placeholder="Select a year"
                />
            </div>

            {/* Animation Time Filter */}
            <div className="flex items-center gap-2">
                <label className="text-sm md:text-lg font-semibold">Animation Time:</label>
                <Select
                    options={animationOptions}
                    value={animationOptions.find((option) => option.value === animationTime)}
                    onChange={(option) => setAnimationTime(option?.value || 5000)}
                    className=""
                    styles={{
                        control: (provided) => ({
                            ...provided,
                            border: "2px solid #22c55e",
                            borderRadius: "0.5rem",
                            boxShadow: "none",
                        }),
                        option: (provided, state) => ({
                            ...provided,
                            backgroundColor: state.isFocused ? "#86efac" : "white",
                            color: "black",
                        }),
                    }}
                    placeholder="Select animation time"
                />
            </div>

            {/* Activity Grid */}
            {Object.entries(groupedData).map(([type, activities], index) => (
                <div key={index} className="p-2 border-2 border-green-500 rounded-lg flex flex-col gap-2">
                    <CanvasGrid
                        polylines={activities.map((a) => a.polyline)}
                        activityType={type}
                        animationTimeMs={animationTime}
                        showActivityType={true}
                    />
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

export function CanvasGrid({
    polylines,
    activityType,
    animationTimeMs: animationTime,
    showActivityType = true,
}: {
    polylines: string[];
    activityType: string;
    animationTimeMs: number;
    showActivityType?: boolean;
}) {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        ctx.imageSmoothingEnabled = false;

        const decodedPolylines = polylines.map(decodePolyline);
        const processedPolylines = decodedPolylines.map((polyline) =>
            customScalePolyline(applyEquirectangularApproximation(polyline))
        );

        const gridSize = Math.ceil(Math.sqrt(processedPolylines.length));
        const borderSizePx = 6;

        const canvasHeight = 1000;
        const canvasWidth = canvasHeight;
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        const squareSize = (canvas.width - (gridSize + 1) * borderSizePx) / gridSize;

        const drawFrame = (startTime: number) => {
            const elapsedTime = performance.now() - startTime;
            const progress = Math.min(elapsedTime / animationTime, 1);

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            processedPolylines.forEach((polyline, index) => {
                const col = index % gridSize;
                const row = Math.floor(index / gridSize);

                const startX = col * squareSize + (col + 1) * borderSizePx;
                const startY = row * squareSize + (row + 1) * borderSizePx;

                ctx.beginPath();
                const pointsToDraw = Math.floor(polyline.length * progress);
                polyline.slice(0, pointsToDraw).forEach(([x, y], i) => {
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

            if (progress < 1) {
                requestAnimationFrame(() => drawFrame(startTime));
            } else {
                requestAnimationFrame(() => drawFrame(performance.now()));
            }
        };

        drawFrame(performance.now());
    }, [polylines, animationTime]);

    return (
        <div className="flex flex-col items-center gap-4">
            <canvas ref={canvasRef} className="border rounded max-h-[80vh] max-w-full" />
            {showActivityType && (
                <div className="text-sm md:text-lg text-center">Activity type: {activityType}</div>
            )}
        </div>
    );
}


function decodePolyline(encoded: string): [number, number][] {
    return polyline.decode(encoded);
}

function applyEquirectangularApproximation(polyline: [number, number][]): [number, number][] {
    const R = 6371;
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
