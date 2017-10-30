Licensed under the MIT License. 

Copyright 2017 RYAN TUBBS rmtubbs@gmail.com 

===================================================================================

COZMO'S WEATHER REPORT

This program allows Anki's Cozmo robot to read aloud the current weather conditions
and provide advice appropriate for the current temperature range. The program 
makes a request from Wunderground's weather API and converts the received JSON data
into text that Cozmo can speak as well as displaying an icon on Cozmo's screen that 
represents the current weather conditions. 

In order to use this program, you must obtain a free API key (a long string of 
characters that uniquely identifies your locational preferences) from Wunderground 
(https://www.wunderground.com/weather/api/) and enter your key below on line 64 
where it says, ENTER_YOUR_API_KEY_HERE. You must also enter the 
TWO_LETTER_STATE_ABBREVIATION and YOUR_CITY name. Be aware that there are several different
Data Feature options when setting up your API key, each of which will return a
different set of JSON data. This program is designed to work with the "conditions"
Data Feature; selecting a different option would require you modify the JSON variable 
settings within this program.  
