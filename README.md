# CalendarScripts
This is folder with some scripts that I use for calendar automatic creation of events


API at use: https://developers.google.com/apis-explorer/#p/calendar/v3/

From here: "console.cloud.google.com/" you can access google's services and look around, 
but for this scrips we will use the calendar google api:
"https://console.cloud.google.com/marketplace/product/google/calendar-json.googleapis.com"

There we will manage the api
Create a credential and a client with OAuth2.0

There will be a step where you can download the credentials in JSON format. Rename it "credentials".

"https://console.cloud.google.com/auth/audience" 
Your email will not have access unless you add it by hand like a "test user"

How to run?
in your console: python "name of script"

Installations:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
