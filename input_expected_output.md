## Introduction
The ADH-Me agent has three main functionalities at the moment:
 - A calendar booking feature
 - A research paper finder
 - A summarizer which summarizes found papers

The calendar booking feature can book 1 or more appointments into your google calendar depending on your request, but only after an user affirmation.
The research paper finder uses the semanticscholar API to find research papers and the summarizer can give a short summary of the research paper in question.

## Inputs
1. "Book a study session tomorrow at 14:00 for 2 hours"
2. "Book a study session the next 4 days at 14:00 for 2 hours"
3. "I need a research paper about Plancks Constant which i can read and review tomorrow between 12:00 and 18:00"
4. "I need to study for an exam that is on tuesday, could you book 5 hours every day from tomorrow untill tuesday from 08:00 to 13:00"


## Expected Outputs
1. The calendar tool will be used and a booking should be created in your calendar with the agent confirming that it is booked.
2. The calendar tool will be used and 4 bookings should be created in your calendar with the agent confirming that they are booked, it also should provide a plan to break down the tasks into smaller manageable tasks.
3. Both calendar and research_tool will be activated. A study about plancks constant will be provided and booking will be made in the calendar for the given time.
4. The calendar tool will book 5 bookings which are each 5 hours long on the given times.
