## Auth Check Endpoint

### Overview

The Auth Check endpoint is designed to provide a simple and effective way to check the operational status of the auth service. This endpoint can be used to validate the integration of this service with the whole application, ensuring that it is running as expected.

### Details

After properly integrating this endpoint with the whole application, you will get an HTTP Get endpoint, `/api/v1/auth/check`, that will return a simple message with the response body, `{"msg": "Auth service is up and running!"}` when requested. This endpoint does not require any sort of authentication or have any dependencies injected. If the aforementioned response is obtained after making the HTTP request, then it can be confirmed that the auth service has been integrated properly with the whole application, and it is ready to be modified to have more endpoints which won't require any further integrations.

### Notes

* The `/api/v1/auth/check` route is entirely an optional route. It can be removed anytime after confirming the integration, this won't affect the application in any way.
