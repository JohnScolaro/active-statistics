export default function RateLimitExceededModal({
  handleExit,
  modalState,
}: {
  handleExit: () => void;
  modalState: boolean;
}) {
  return (
    <>
      <div
        className={`top-0 left-0 w-full h-full backdrop-blur-sm opacity-75 ${
          modalState ? "fixed" : "hidden"
        }`}
      ></div>
      <div
        className={`absolute items-center top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-green-400 p-2 rounded-lg ${
          modalState ? "absolute" : "hidden"
        }`}
      >
        <div className="p-2 bg-white rounded-lg flex flex-col">
          <div className="text-6xl text-center">😢 Oh no! 😰</div>
          <div className="h-4"></div>
          <div>
            I&apos;ve exhausted my Strava API limit. Please check back again later.
          </div>
          <div className="h-10"></div>
          <button
            type="button"
            className="bg-green-400 p-2 rounded-lg"
            onClick={handleExit}
          >
            Close
          </button>
        </div>
      </div>
    </>
  );
}
