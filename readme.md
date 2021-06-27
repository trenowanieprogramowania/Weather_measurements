## Weather measurement analyser (author: trenowanieprogramowania)

---

### Introduction

Python 3 implementation of air pollution analysis in Poland
based on extracted data from API stored at:
- http://powietrze.gios.gov.pl/pjp/content/api
- https://openweathermap.org

---

### General Content

The analysis is based on the extraction of data from stations available from http://powietrze.gios.gov.pl/pjp/content/api.

The data are enriched by further details available from API stored at https://openweathermap.org


Given analysis on elementary level includes:
- value of chemical compounds registered within hour period (including updated results)
- specific location of station with an accuracy of up to street address
- updates of registrations per hour
- general description of air quality based on the temporary amount of detected chemical compounds
- pressure of air in the locations of stations


Note: Software works without GUI, in CLI mode.

---

### How software works

1.) Software sends GET request to API available at http://powietrze.gios.gov.pl/pjp/content/api. 

2.) As a result of request, the following data are obtained:
- specific information of stations registered by given API
- specific information of measurement points associated with each station
- values of records registered by each measurement point

3.) Collected data are processed within the structure of OOP paradigm and stored into list.

4.) Processed data are converted into data frame further manipulated by Python framework "Pandas"

5.) The inclusion of additional data is performed by sending additional GET request to API stored at 
https://openweathermap.org. The additional columns of given data frame are constructed.

6.) The analysis of air quality is conducted and column describing air quality is derived.

7.) The results are presented in IDE's terminal in the form of data frame.

---

### Required Python packages
- matplotlib~=3.4.2
- numpy~=1.20.2
- pandas~=1.2.3
- requests~=2.25.1
---

### Additional features
a) output adjustments
- software has a possibility of scaling number of samples extracted from main API http://powietrze.gios.gov.pl/pjp/content/api
- the application has a feasbility of including additional columns of data extracted from API https://openweathermap.org
  (humidity, air's temperature, average wind speed)
  
  
b) optimisations
- programme has a possibility of selecting faster version of data manipulation that relies on using "loc" method from
  "Pandas" library (selecting data_manipulation_with_loc_method)
- user can select which version of programme to download (with acceleration or without)
- there is additional possibility of setting flaque "latest" to include only most updated data extracted from
measurement points (by default, all data are extracted from API from selected number of samples)
  
c) visualisation of optimisation
- software has a capability of drawing relationship between "naive" methods and those based on "Pandas" methods
  (note: current version is restricted to comparing air quality analysis with or without "loc" method)
- relevant functions are available in module "extra_activities"

d) visualisation of extracted data
- software owns a possibility of visualisation of extracted data
- relevant functions are stored in module "actions_applied_to_data" (file "data_presentation")

---

### Preliminaries

It is assumed that user installed the following components on PC:
1. Python version 3.7 (or higher) (for the interpreter to work)
2. Python IDE (Visual Studio Code, Pycharm, Netbeans)


Software works on each standard OS (Windows, Linux, Mac) - no need to specify particular dependencies for particular
OS.

---

### Usage

To run this programme, it is recommended to have on PC
at least 17 MB of RAM.

---

### Building

- Option 1

| No. of step   | Description   |
| ------------- |:-------------:|
| 1. | Download the ZIP file. |
| 2. | Extract it to a repository of desired choice. |
| 3. | From prompt/console create virtual environment by executing the command <br> `python3 -m venv /path/to/new/virtual/environment`
 |
| 4. | From prompt/console select path of repository.|
| 5. | At given path of repository type in CLI <br>`pip install requirements.txt` |
| 6. | Type `python3 main.py`

Note: to specify parameters one should in "main.py" file modify input parameters for different outcomes to obtain (e.g. different number of samples)

- Option 2

| No. of step   | Description   |
| ------------- |:-------------:|
| 1. | In Git CLI type <br>`git clone https://github.com/trenowanieprogramowania/Weather_measurements.git` |
| 2. | From prompt/console select path of repository.|
| 3. | From prompt/console create virtual environment by executing the command <br> `python3 -m venv /path/to/new/virtual/environment`
 |
| 4. | At given path of repository type in CLI <br>`pip install requirements.txt` |
| 5. | Type `python3 main.py`|

---
### About author
Further information about the author can be found at LinkedIn platform:
https://www.linkedin.com/in/jacek-piekut/