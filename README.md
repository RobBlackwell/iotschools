# IoT Schools Weather Network

A prototype web site for exploring weather data from the IoT Schools
project via the Xively platform.

Deployed at http://iotschools.azurewebsites.net

## Background

This web site was developed as part of a Cranfield University MSc
Group Project with Innovation Peterborough in March 2016.

In studying the water quality of the Werrington Brook and surrounding
area, We wanted to retrieve data from the IoT weather stations based
at schools around Peterborough. We found the existing
http://iotschools.org.uk/ to be difficult to use for historic data
download, but all the data is stored and accessible via
https://xively.com/.

The site is built using Python3 and Flask.

The design is based on [Skeleton](http://getskeleton.com/).

The site is hosted on Microsoft Azure using a free DreamSpark for
students subscription.

We've focussed on Peterbrorough, but the
http://iotschools.azurewebsites.net/advanced.html page allows easy
access to IoT schools in other parts of the world. It would be easy to
fork this code and do something custom for another area or specific
school.

Please send me pull requests.

## Ideas / TODO

Enable caching of Xively queries, probably using werkzeug.contrib.cache    
Add graphs and charts (probably using matplotlib)    
Consider http://what3words.com/ integration    
Consider Excel export rather than CSV    
School dashboard page    
Can we do basic weather forecasting?    
Better timeout and error handling when calling the API    
Display dates in a more readable way    
Consider importing other content from iotschools.org.uk including info about the AWSs.    
Include photos and metadata about each site    

Rob Blackwell <rob.blackwell@cranfield.ac.uk>    
March 2016
