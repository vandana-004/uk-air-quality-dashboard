Sprint 3
Duration: Week 8
Scrum Master: Vandana

Sprint Goal:
To complete all remaining data preparation tasks, integrate the cleaned dataset into the dashboard, and implement core visualisation features including seasonal analysis, AQI categorisation, time series trends, weather correlation, and city comparison, bringing the dashboard to a fully functional state ready for final testing.

User Story 1(Medium) (Nikhil):

As a user, I want to see an AQI label on readings so I can quickly tell whether the air quality is safe or not. 

Tasks
Add an aqi_category column: Low, Moderate, High, Very High
Double check the thresholds match UK standards

Estimated Effort: 4-5 hours


User Story 2(Medium)(Vandana): City comparison

As a student, I want to see how pollution has changed over time so I can spot long term patterns.

Tasks
Build a line chart using the date column
Add a dropdown so users can pick which pollutant to view
Make sure it updates when the selection changes

Estimated Effort: 7-8 hours





User Story 3(High) (Vandana):

As a user, I want to know which city has the worst air quality so I can see the biggest problem areas at a glance.

Tasks
Calculate average pollutant values grouped by city
Build a horizontal bar chart ranked from worst to best
Highlight the top city somehow: colour, label, or both

Estimated Effort: 5-6 hours


User Story 4(Medium) (Semih):
As a researcher I would like to be able to quickly see (view) summary statistics for mean, min and max values for all pollutants in my data set, to give me an overall impression of the data.


Tasks
For each pollutant calculate the mean, min, max and the Standard Deviation
Show these as a summary table or as info cards on your dashboard
Provide users with the ability to filter the data based on City and Date Range
Estimated Effort: 4-5 hours

User Story 5(Medium) (Semih):
As a new user, I would like to be able to view a brief description of each pollutant (NO2, PM2.5, CO and Ozone), so I may better comprehend how each pollutant impacts my health.


Tasks
Write a few lines of plain English for each pollutant
Include an information icon (info) adjacent to each pollutant's label on the dashboard
Show the description in either a tool tip or popup window when the icon is clicked
Estimated Effort: 3-4 hours


Sprint Outcome:

Sprint 3 was an opportunity to make the analysis in the Air Quality Dashboard more understandable for users by including a pollution risk classification and additional comparison type visualization.
