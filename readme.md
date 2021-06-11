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

Given analysis includes:
- value of chemical compounds registered within hour 
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

4.) Processed data are converted into data frame.

5.) The inclusion of additional data is performed by sending additional GET request to API stored at 
https://openweathermap.org. The additional columns of given data frame are constructed.

6.) The analysis of air quality is conducted and column describing air quality is derived.

7.) The results are presented in IDE's terminal in the form of data frame.

---

### Required Python packages
- jakie biblioteki sa wymagane (wymienic wszystkie wymienione zaimportowane)
---

### Additional feature of the software
- opisac, co mozna znalezc w punkcie "other_api_extraction"
- wspomniec funkcje flagi "latest" (wspomniec o optymalizacji) (zawrzec jako 2 punkt po "intro")
- wpisac mozliwosci dopasowania programu (np. liczba pobieranych probek)

---

#dodatkowo
- wkleic zrzuty ekranu (z krotkimi opisami)

---

### Preliminaries

It is assumed that user installed the following components on PC:
1. Python version 3.7 (or higher) (for the interpreter to work)
2. Python IDE (Visual Studio Code, Pycharm, Netbeans)

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
| 3. | From prompt/console select path of repository.|
| 4. | Type `python3 main.py`

- Option 2

| No. of step   | Description   |
| ------------- |:-------------:|
| 1. | In Git CLI type `git clone https://github.com/trenowanieprogramowania/Weather_measurements.git` |
| 2. | From prompt/console select path of repository.|
| 3. | Type `python3 main.py`|


### About author
Further information about the author can be found at LinkedIn:
https://www.linkedin.com/in/jacek-piekut/