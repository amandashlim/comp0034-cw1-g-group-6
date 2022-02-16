# Visualisation 3: The Line Chart

The target audience for our map visualisation is anyone who is either moving to or living in London, who is interested in learning about and comparing the crime rates for each form of crime in the different london boroughs.

The line chart visualisation is intended to address are the following questions:

    1. How has drug crime evolved in London over the two recorded years?
    2. How does sexual offence fluctuate over the four seasons?

![Map](../assets/line_chart.png)

### *1. Explaining the design*

We created a line chart in order to answer the two questions previously stated. 
The line chart allows users to see the fluctuation of the incidents of a crimes over months, which could allow them to observe a pattern seasonally.

Once again, we included the option to select filters on the left-hand side of the dashboard, where users are able to specify which crime they are interested in gaining insights on.
This aspect provides our webapp users with the option to personalise their crime searches.

### *2. Evaluating the design*

To create the line chart, we used multiple datasets. The main dataset used was the Metropolitan police dataset (crime_data.csv).
We also used other datasets so that users could look at the line chart through different population data as we can see in the filters on the left-hand side of the dashboard.
The other datasets used were for raw data (population.csv), population - 2020 GLA estimate (pop2020_df_r.json), population - 2011 Census (pop2011_df_r.json), workday population (workday_df_r.json), predictions made with fbprophet (df_r.json) and total daytime population (daytime_df_r.json and daytime_population.csv). 

We used the multiple datasets to provide a line chart visualisation that answers all the aforementioned target audience questions.

Webapp users are able to select a form of crime as well as one or multiple boroughs.
For each form of crime, we added a line to show the average crime rate for the corresponding form of crime.
Then, for each form of crime we have a personalised line which shows the counts of crime over the months recorded.
However, in the dataset provided, there were missing counts for some of the most recent months. This was a limitation. 
We overcame this by forecasting the data for the more recent months by also adding upper and lower bounds.
This visualisation is effective at measuring the evolution of crime over time as it shows the webapp users the fluctuation of the crime count - This helps us answer the target audience questions.
On the right-hand side of the dashboard we also included statistics showing the boroughs with the highest and lowest average and recorded crime rates for the selected crime. 
This is useful as it allows users to compare the boroughs they selected with the extremes of the form of crime selected.

Although the feature that allows users to add multiple boroughs is useful to compare the crime rates across the timeline, adding multiple boroughs clutters the line chart and makes it more confusing for the user. 
Our solution to this weakness of the visualisation is to limit the number of boroughs users can select to three. 
Another weakness is that we didn't create the option to look at the line chart data seasonally. 
By providing an option to change the dates to seasons, we could allow for the users to see more precisely whether the occurrences of crime rates are seasonally linked.
