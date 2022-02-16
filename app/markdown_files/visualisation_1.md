# Visualisation 1: The Map

The target audience for our map visualisation is anyone who is either moving to or living in London and hence, is looking for somewhere to live. The target audience wants to learn and compare the crime rates in the different london boroughs. Furthermore, they are looking for insights into the occurrences of different forms of crime.

The map visualisation is intended to address are the following questions:

    1. How has drug crime evolved in London over the two recorded years?
    2. Which borough has the highest crime rates in London?

![Map](../assets/map.png)

### *1. Explaining the design*

We chose to create a map as it is an effective visualisation for our webapp users to compare the London boroughs' crime rates. This is because a map is intuitive and fit for interactivity. 
Simply reading the data in numeric form would make it difficult for users to grasp a true visual understanding of the crime rates in different boroughs as users would not understand the context of each measurement of crime as part of a whole picture in London.
A map allows users to compare the crime rates using a colour spectrum system, where the colour purple signifies a low crime rate and the colour yellow signifies a high crime rate.

We added functionality by providing users with a slider, allowing them to see how the crime rates have evolved over the recorded months.
Therefore, for specific boroughs, users will notice the colour change and gain insight into how crime rate in that area has increased or decreased over a decided time period.

Finally, on the left-hand side of the dashboard, we can see that there is a section enabling users to select filters in relation to the types of crime.
These filters allow our webapp users to tailor their map to their preferences.

### *2. Evaluating our visualisation*

To create the map, we used multiple datasets; the main datasets were the Metropolitan police dataset (crime_data.csv) and a London Borough dataset (london_boroughs.json) to create the map.
We used other datasets to provide additional insights by allowing users to look at the map through different population datasets. This can be observed in the filters on the left-hand side of the dashboard.
The other datasets used were for raw data (population.csv) and total daytime population (daytime_population.csv). 

For the map, we used all the data from each dataset listed above to answer our 2 questions stated above.

The map is extremely useful to users, as it offers an intuitive and interactive way to learn about the crime rates in each London borough.
We added more functionality by including a feature where users can hover their mouse over a borough and provide them with summary of information on the borough. This summary includes the borough name and the crime level for the selected crime category.
If the user wishes to receive more detailed information on the borough or boroughs selected, they simply need to click on the borough(s) they are interested in and statistics on the selected borough(s) will show on the right-hand side of the screen.
The statistics provides numerical values to show how the crime rate has changed since the previous month, the last 3 months and over the last year. This allows users to observe how the crime rates have improved or worsened over the chosen timeframe.
These features are all strengths of the webapp as it allows the user to be provided with global data, which is easy to understand. However, if they wish to understand the crime intricacies over each borough, they simply need to click on the borough to view the insights. 

A weakness of the map is that we are unable to provide users with a map where the date selected is "Today". This is because we have not been provided with this data.
If were able to have access to this data, we could improve the map by enabling it to fetch data in real-time and update the map constantly so that users would have access to the latest crime information of London.
Moreover, it would have been interesting to compare the London data to other locations within the UK. Webapp users would have a more contextualised understanding on the crime data to better determine whether the crime rates should be considered as low or high in relation to areas outside of London.

Another weakness are the tradeoffs we had to make. 
* One tradeoff is between a static legend/color range and a dynamic one: 
  * A static legend/color range would provide the user a better 
  understanding of how exactly the crime changes through time, as all the boroughs' colors would brighten if the crime overall reduced, which would 
  make it easier to compare the crime rates between the months. 
  * A dynamic legend/color range, as is the one implemented now, provides the user a better understanding of the relationships of comparisons between boroughs,
as for each month the color range is specific to that month and shows the areas with relatively similar crime rate rankings with a similar color.

The tradeoff is between being able to visually see the time range changes in crime rate in the same color range which would clearly show when crime overall decreases/increases,
however this would make boroughs in months with more uniform crime rate across the board harder to distinguish.
And between being able to clearly distinguish each month's boroughs with the highest/lowest crime rate, which compromises on clarity when scrolling through time.
Because, we're implementing a line visualization which will clearly show the crime rate movement between the months, we decided that for the map visualization the 
dynamic legend/color range would be more appropriate. 

* Another tradeoff is between a plotly embedded date slider and a dash slider element.
  * A plotly embedded date slider, created with animation frames, is overall smoother to use and has a feature to play thorough the months, which 
is great to see how crime rate changes through time. However, currently there is no reasonable way of getting the information about the animation frame (our case month), which
makes Dash integration with it impossible, meaning the date selected couldn't update the statistics panel
  * A dash slider element is overall more choppy and lacks the ability to play through, but provides us with the opportunity to create callbacks
for it and integrate it with other parts of the app

Because we already agreed on a dynamic legend/color range as mentioned above, the playing of the animation with plotly embedded date slider could be confusing,
as not only the colors would change but the weighting on them as well (meaning that lighter color than before might not mean lower crime rate). Given that and the 
importance of the statistics panel, we decided to use a dash slider element for selecting the date.
