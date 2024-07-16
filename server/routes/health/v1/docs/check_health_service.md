## Health Check Endpoint

### Overview

The Health Check endpoint is designed to provide a simple and effective way to check the operational status of the application. This endpoint can be used to validate the availability of the application, ensuring that it is running as expected with the correct configuration.

### Details

This endpoint provides users with an HTTP Get endpoint, `/api/health`, that will return a simple message with the response body, `{"msg": "The application is up and running!"}` when requested. This endpoint does not require any sort of authentication or have any dependencies injected. If the aforementioned response is obtained after making the HTTP request, then it can be confirmed that the application has been configured properly, and it is healthy.

### Notes

* The `/api/health` route is to be used by application load balancer to verify the availability of the application so that it can forward client requests to this server.
