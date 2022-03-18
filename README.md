# COMP0034 Coursework 1
## Group 6
### Crime Rate in London dataset


GitHub Link to Repo:[https://github.com/ucl-comp0035/comp0034-cw1-schema-group-6](https://github.com/ucl-comp0035/comp0034-cw1-g-group-6)

Link to App Design Explanation: [design_explanation.md](crime_flask_app/crime_dash_app/markdown_files/design_explanation.md)

#
#### Note about requirements.txt:

All dependencies used are in the [requirements.txt](requirements.txt), however [***pystan***](https://pystan.readthedocs.io/en/latest/) 
and [***prophet***](https://facebook.github.io/prophet/docs/installation.html#python) are commented out
because Windows machines require a C++ interpreter and a separate conda environment to install and 
run ***pystan*** and ***prophet*** and some older 
computers start lagging when trying to install them. 

As the app was designed in a way where using the ***prophet*** is unnecessary, 
as the predictions are stored in .json files, we purposefully commented out the packages so to not interfere.
However, if you wish to run the predictions yourself feel free to uncomment them or install them by yourself.

### Link to Video

Here is the link for a video showcasing our dash app:
[https://youtu.be/ufafiY_zjP0](https://youtu.be/ufafiY_zjP0)