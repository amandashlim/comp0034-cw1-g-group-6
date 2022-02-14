# Visualisation 1: The Map

The target audience for our map visualisation is anyone who is either moving to or living in London, who is interested in learning about and comparing the crime rates for each form of crime in the different london boroughs.

The questions that this visualisation is intended to address are the following:

    1. How has drug crime evolved in London over the two recorded years?
    2. Which borough has the highest crime rates in London?

![Map](../assets/map.png)

### *1. Explaining the design*

We chose to create a map as we believe that it is the most effective visualisation for our webapp users to compare the London boroughs' crime rates. 
Simply reading the data in numeric form would not allow them to grasp an informed understanding on the crime rates as they would not be able to figure out whether the numbers given are supposed to be considered as high or low.
A map allows them to compare the crime rates where on the low end of the spectrum, which is in purple, means that there is a low crime rate and on the high end of the spectrum, which is in yellow, which means that there is a high crime rate.

We also decided to provide our users with a slider, allowing them to see how the crime rates have evolved over the recorded months.
Therefore, if they are looking at a specific borough they are interested in, they can see the colour change and find out if the crime rate in that area has increased or decreased over the months.

Finally, on the left-hand side of the dashboard, we can see that there is a section enabling users to select filters in relation to the types of crime.
These filters allow our webapp users to tailor their map to their preferences.

### *2. Evaluating our visualisation*

To create the map, we used multiple datasets; the main datasets used were the Metropolitan police dataset (crime_data.csv) and a London Borough dataset (london_boroughs.json) so that we could create the map.
We also used multiple other datasets so that users could look at the map through different data on the population as we can see in the filters on the left-hand side of the dashboard.
The other datasets used were for raw data (population.csv), population - 2020 GLA estimate (pop2020_df_r.json), population - 2011 Census (pop2011_df_r.json), workday population (workday_df_r.json) and total daytime population (daytime_df_r.json and daytime_population.csv). 

For the map, we used all the data from each dataset listed above to answer the questions.

The map is extremely useful to the users, as it is the simplest and most interactive way for them to learn about the crime rates in each London borough.
We decided to add a feature where users can hover their mouse over a borough and provide them with **condensed?? idk what word to use** information on the borough which is the borough name and the amount of crime for the type selected by the user.
If the user wishes to get more **longer???** data on the borough or boroughs selected, they simply need to click on the borough(s) they are interested in and statistics on the selected borough(s) will show on the right-hand side of the borough.
These features are all strengths of the webapp as it allows the user to be provided with global data, which is easy to understand. However, if they wish to have more in depth data, they simply need to click on the borough to see it. 

A weakness of the map is that we are unable to provide users with a map where the date selected is "Today", as we are not provided with the data.
If were able to have access to this data, we would try to improve the map by enabling it to fetch data in real-time and update the map constantly so that users would have access to the latest crime data in the London boroughs.
Moreover, it would have been interesting to be able to compare the London data to other locations within the UK, so that webapp users can have a broader understanding on the crime data to better determine whether the crime rates should be considered as low or high in relation to areas outside of London.
