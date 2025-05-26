# Welcome to ADH-Me

To get the project up and running you will have to setup a few things. As this is a proof of concept project, security and userfriendlyness has not been prioritized, but we hope you will enjoy the application anyway.

**Warning! If you fork this project, please remember not to push any of your credentials or secrets to your repository.**

## Setup Google API for your Calendar
1. Follow this link for a step by step guide on how to setup the Google API for your Calendar: https://developers.google.com/workspace/calendar/api/quickstart/python, we will also go through the setup here:
2. Create a Google Cloud Project https://console.cloud.google.com/projectcreate
3. When on the dashboard of your Google Cloud Project, navigate to API & Services > Enabled APIs & Services
4. Click the Enable APIs and services and click on the Google Calendar API, and the press Enable.
5. Navigate to API & Services > OAuth consent screen
6. Click Branding, and Get started
7. Fill out Name, and place your email inside the User support email.
8. In Audience choose External **[NOTICE THIS DIFFERS FROM GOOGLES OWN SETUP]**
9. In Contact info place your email
10. Agree to Google API Services: User Data Policy
11. Navigate to Clients
12. Click "Create client"
13. Choose Desktop App and name it
14. A new window will appear and there will be a button at the bottom where it says "Download JSON", click it
15. Click OK once the download is done
16. Rename the file you have downloaded to credentials.json, and save it for a later step.

## Setup ADH-Me
1. Clone the repository and open it.
2. Run ```pip install requirements.txt```
3. Run ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
4. Run the file calendar_agent
