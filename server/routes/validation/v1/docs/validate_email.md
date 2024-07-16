## Endpoint to check the availability of email address

### Overview

This endpoint is provided to validate the availability of the email address required to be included as a query parameter for the registration of a new user account. This will return `true` if the email can be registered, or `false` if the email has already been used.

### Details

This endpoint is to be used on the client-side application before making the `/api/v1/auth/signup` request. It is suggested to disable the `Submit` button for the signup form as long as a *truthy* response is not obtained by using this endpoint. A common way to use this can be when the email form field goes out of focus. The response from the backend will contain the needed prompt to be shown to be user when the email is not available to be used. When available, a common way to let the user know is to use a green tick on the right-hand side.

### Notes

* Availability of this endpoint does not leave the `/api/v1/auth/signup` endpoint defenseless as to allow using already used up email address.

* Database table has the `unique` constraint implemented for maintaining data integrity.
