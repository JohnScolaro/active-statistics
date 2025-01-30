/*
Just a function that wraps the fetch function so I don't need to handle errors
and auth issues everywhere.
*/
export function wrappedFetch(
  url: string,
  successCallback: (data: any) => void,
  errorCallback: (err: Error) => void,
  router: any,
) {
  fetch(url, {
    method: 'GET',
    credentials: 'include', // Include cookies in requests
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      // If we get a 401 status, redirect to home and throw an error.
      if (response.status === 401) {
        router.push("/");
        throw new Error("Unauthorized: 401");
      }

      // For any non-200 responses, throw an error.
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      // Otherwise, parse the response as JSON.
      return response.json();
    })
    .then(
      (data) => successCallback(data),
      (err) => {
        console.error(err);
        errorCallback(err);
      }
    )
    .catch((err) => {
      console.error(err);
      errorCallback(err);
    });
}
