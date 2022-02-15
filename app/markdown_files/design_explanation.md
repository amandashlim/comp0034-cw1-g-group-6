# Visualisations Design Explanations

In this project, we set out to create an insightful and well-functioning Dash App for our dataset. To achieve this, we made three different visualisations to answer our target audience questions.
In coursework 1 of COMP0035, we detailed these questions relating to the Metropolitan Police dataset and have been listed below:

    1. How has drug crime evolved in London over the two recorded years?
    2. Which type of crime is the highest and lowest in London?
    3. How does sexual offences fluctuate over the four seasons?
    4. Which borough has the highest crime rates in London?

To answer these questions, we narrowed the scope of our data exploration to three categories visualisations. These were:

    1. A chloropleth map
    2. A histogram
    3. A line chart

Each of these visualisations are able to answer one or multiple of the aforementioned target audience questions. 
jjj
To explain the design of our visualisations clearly, we will first obtain a solid understanding of our target audience and their needs.

### 1. Target Audience

![Persona](../assets/persona.png)

Our target audience for the webapp, are university students who are new to London and looking for accommodation.
Since our target audience is assumed to not know London, the webapp would be useful as it would allow them to be informed on the crime rates associated with each London borough.
Moreover, based on personal preferences, they would be able to tailor their searches to the crimes they are more concerned about.

### 2. Visualisation 1: The Map

[Visualisation 1: Link to design explanation and evaluation](../markdown_files/visualisation_1.md)

### 3. Visualisation 2: The Histogram

[Visualisation 2: Link to design explanation and evaluation](../markdown_files/visualisation_2.md)

### 4. Visualisation 3: The Line Chart

[Visualisation 3: Link to design explanation and evaluation](../markdown_files/visualisation_3.md)

### 5. Testing the Dash App

To test the dash app, we came up with 2 separate tests using selenium.
The first test, checks to see that, given the app is running, when we access the homepage, the H1 heading of the webapp is "London Crime Rates".
The second test is that given the app is running, when we access the homepage, then there should be written "Select Chart Type".

** will there be a third???

[Link to tests with selenium](tests/test_crime.py)

We also came up with unit tests. 





