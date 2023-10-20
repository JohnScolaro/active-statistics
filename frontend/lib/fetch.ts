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
    fetch(url)
      .then(
        (response) => {
          // If we are getting auth errors from hitting an endpoint, just redirect to home because we need to log in again.
          if (response.status == 401) {
            router.push("/");
            throw new Error("Unauthorized: 401");
          }
          return response.json();
        },
        (err) => {
            console.log(err);
        },
      )
      .then(
        (data) => successCallback(data),
        (err) => {
          console.log(err);
          errorCallback(err);
        },
      );
  }
