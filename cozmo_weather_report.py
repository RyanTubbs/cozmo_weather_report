#!/usr/bin/env python3

# Licensed under the MIT License. 
#
# Copyright 2017 RYAN TUBBS rmtubbs@gmail.com 
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions: 
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

# COZMO'S WEATHER REPORT
# This program allows Anki's Cozmo robot to read aloud the current weather conditions
# and provide advice appropriate for the current temperature range. The program 
# makes a request from Wunderground's weather API and converts the received JSON data
# into text that Cozmo can speak as well as displaying an icon on Cozmo's screen that 
# represents the current weather conditions. 

# In order to use this program, you must obtain a free API key (a long string of 
# characters that uniquely identifies your locational preferences) from Wunderground 
# (https://www.wunderground.com/weather/api/) and enter your key below on line 64 
# where it says, ENTER_YOUR_API_KEY_HERE. You must also enter the 
# TWO_LETTER_STATE_ABBREVIATION and YOUR_CITY name. Be aware that there are several different
# Data Feature options when setting up your API key, each of which will return a
# different set of JSON data. This program is designed to work with the "conditions"
# Data Feature; selecting a different option would require you modify the JSON variable 
# settings within this program.  

import cozmo #Imports the 'cozmo' module from Cozmo's API, which enables this program to access Cozmo's core capabilities.
import urllib.request #Imports the Python 'urllib.request' module so the program can open the API URL.  
import json #Imports the Python 'json' module so the program can interpret the JSON data received from Wunderground. 
import requests #Imports Kenneth Reitz's 'requests' module for Python. It's similar to 'urllib.request', but offers higher-level functionality. 
from io import BytesIO #Imports the Python 'BytesIO' module to interpret binary data from the weather conditions icon.  
try: #Imports the Pillow 'Image' module for Python to help display the icon image on Cozmo's face. 
    from PIL import Image
except ImportError: #Error notification and instructions if the end user has not previously installed Pillow.  
    sys.exit("Cannot import from PIL. Do `pip3 install --user Pillow` to install") 

def get_in_position(robot: cozmo.robot.Robot):
    #This function is borrowed from Anki's SDK examples. It adjusts Cozmo's head so that his face can be easily viewed. 

    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

def weather_advice(robot: cozmo.robot.Robot):
    #This is the main function within the program; it contains the API request, JSON conversion, and image processing,
    #allowing Cozmo to read the weather report and display the weather icon.  
    
    get_in_position(robot) #First we call the 'get_in_position' function (defined above) so we can see Cozmo's face.             
    with urllib.request.urlopen("http://api.wunderground.com/api/ENTER_YOUR_API_KEY_HERE/geolookup/conditions/q/TWO_LETTER_STATE_ABBREVIATION/YOUR_CITY.json") as url: 
    #This line includes the actual API call to Wunderground's server using the 'urllib.request' module. If you paste this URL into 
    #your browser, you should be able to see the raw, nested JSON data, which is helpful for understanding where we pull our data from
    #in the variables we declare below. Be sure to customize the URL with your API key, two-letter state abbreviation, and city name!   

        parsed_json = json.loads(url.read().decode()) 
        #We now take the received JSON data and convert it into a format we can utilize in Python by using the .loads, .read, and 
        #.decode methods from the 'json' module. We also place these converted data into a variable named 'parsed_json' so we can  
        #manipulate the data in the lines that follow.

        temp_f = parsed_json['current_observation']['temp_f'] 
        #We declare another variable named 'temp_f' that pulls the current temperature from the nested data we just converted above.
        #This variable returns an integer, which Cozmo cannot speak aloud, but he utilizes it as a parameter within the program.  

        temperature = str(parsed_json['current_observation']['temp_f'])
        #This variable accesses the same data as the 'temp_f' variable, but here we convert it to a string (words/text) using the str method 
        #so that Cozmo can say the temperature aloud. 

        weather = parsed_json['current_observation']['weather'] 
        #Another variable like the one above, but this time returning a short string describing the general weather conditions. These data are 
        #already in the form of a string, so Cozmo can speak this without converting it with str.  

        wind = parsed_json['current_observation']['wind_string']
        #Another variable string, this time describing the wind conditions. 

        icon = parsed_json['current_observation']['icon_url']
        #This variable pulls the URL for the icon that represents the current weather conditions from our nested data. 

        r = requests.get(icon)
        #Now we create a variable that uses the .get method from the 'requests' module to access the icon URL, 
        #which we get by calling the 'icon' variable we just created above. 

        raw_image = Image.open(BytesIO(r.content))
        #The next step is to convert the binary data into an image using 'BytesIO' and open it using the 'Image' module; we set this result as
        #a 'raw_image' variable.  
        
        resized_image = raw_image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC) 
        #We call our 'raw_image' variable and make it fit Cozmo's screen using the .resize method from the 'cozmo' module. 
        #The 'Image.BICUBIC' parameter seems to display the image best on Cozmo's face, although it will display without it. 

        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True, pixel_threshold=175) 
        #We finally have an icon image that will display on Cozmo's screen! The invert_image parameter displays the icon as an outline on a black
        #screen. A pixel_threshold of around 175 seems to display the icon cleanly; the default pixel_threshold of 127 will not display the image.

        action1 = robot.say_text("Right now the weather is " + weather + "." + "The wind is " + wind + "." 
            +  "The temperature is currently " + temperature + "degrees Fahrenheit.") 
        #Now we're almost ready for action! We use Cozmo's .say_text method to assemble a variable string for Cozmo to speak. We combine text  
        #(within quotations) with the strings from our 'weather', 'wind', and 'temperature' variables to produce the three sentences that make 
        #up the weather report.

        action2 = robot.display_oled_face_image(face_image, 5000.0)
        #We create a variable that tells Cozmo to display the 'face_image' variable on his screen for 5000 milliseconds which, unsurprisingly, 
        #works out to 5 seconds. One of the default parameters for this method is in_parallel=True, which allows the image to display on Cozmo's
        #face while he speaks, rather than waiting until he's done.  

        action1.wait_for_completed()
        #Tells the program to wait until 'action1' is done before proceeding. 

        action2.wait_for_completed()
        #Tells the program to wait until 'action2' is done before proceeding. 
        
        if temp_f < 40:
        	robot.say_text("It is cold outside right now. You should wear a jacket to prevent system failure!").wait_for_completed()
        if 40 <= temp_f < 60:
            robot.say_text("It is cool outside right now. You might want a sweater to maintain proper operating temperature.").wait_for_completed()
        if 60 <= temp_f <= 80:
        	robot.say_text("It is a comfortable temperature for humans outside right now.").wait_for_completed()
        if temp_f > 80:
        	robot.say_text("It's pretty hot right now. Don't overheat your circuits!").wait_for_completed()
        #Lastly, we use a series of if statements, our 'temp_f' variable, and some comparison operators to create four different phrases that Cozmo
        #speaks depending on the current temperature.  

cozmo.run_program(weather_advice)
#Tells the program to actually run our 'weather_advice' function.  