# Visualisation 3: The Line Chart

The target audience for our map visualisation is anyone who is either moving to or living in London, who is interested in learning about and comparing the crime rates for each form of crime in the different london boroughs.

The line chart visualisation is intended to address are the following questions:

    1. How has drug crime evolved in London over the two recorded years?
    2. How does sexual offence fluctuate over the four seasons?

![Map](../assets/line_chart.png)

### *1. Explaining the design*

We created a line chart in order to answer the two questions previously stated. 
The line chart allows users to see the fluctuation of the incidents of a crimes over months, which could allow them to observe a pattern seasonally.

We also created crime rate predictions for a specific crime in a specific borough for the next 6 months, this heavily aligns 
with our target customers' goals as we identified their main drive is moving to London, so seeing how a particular crime rate is forecasted
to change in the upcoming months is insightful.

The predictions were done with [Facebook's Prophet](https://facebook.github.io/prophet/) a time series forecasting model. 
This model was used because it was already trained, which in our case where we only have about 2 years worth of monthly data is incredibly
important as training the model ourselves most likely wouldn't produce any reasonable results. Another reason in favor of Prophet is that it works
well with detecting seasonality, which is closely tied with our target audience requirements and business questions.

Once again, we included the option to select filters on the left-hand side of the dashboard, where users are able to specify which crime they are interested in gaining insights on.
This aspect provides our webapp users with the option to personalise their crime searches.

### *2. Evaluating the design*

To create the line chart, we used multiple datasets. The main dataset used was the Metropolitan police dataset (crime_data.csv).
We also used other datasets so that users could look at the line chart through different population data as explained in the main 
readme and seen in the Select Data filter on the left-hand side of the dashboard.

We used the multiple datasets to provide a line chart visualisation that answers all the aforementioned target audience questions.

Webapp users are able to select one type of crime as well as one or multiple boroughs, the decision to use only one crime type was 
taken to de-clutter the line chart, as if multiple crimes and boroughs were selected the visual would be indecipherable.

For each type of crime, we added a line to show the average crime rate for the corresponding form of crime across all boroughs.
Then, for each form of crime we have a personalised line which shows the counts of crime over the months recorded.

As mentioned before, we also forecasted the crime rates for 6 months in advance, which both limits the limitation of not having data on recent months and informs the user about the trends,
which are complemented with confidence intervals to show the uncertainty of predictions. 

This visualisation is effective at measuring the evolution of crime over time as it shows the webapp users the fluctuation of the crime count - This helps us answer the target audience questions.
On the right-hand side of the dashboard we also included statistics showing the boroughs with the highest and lowest average and recorded crime rates for the selected crime type. 
This is useful as it allows users to compare the boroughs they selected with the extremes of the form of crime selected.

Although the feature that allows users to add multiple boroughs is useful to compare the crime rates across the timeline, adding multiple boroughs clutters the line chart and makes it more confusing for the user. 
This weakness could be solved by limiting the number of boroughs users can select or hiding the newly selected boroughs by default, so the user
has to manually toggle their visibility in the legend - both of those things would improve the readability but slightly increase the complexity. 

The second weakness is that we didn't create the option to look at the line chart data seasonally. 
By providing an option to change the dates to seasons, we could allow for the users to see more precisely whether the occurrences of crime rates are seasonally linked and if there is a pattern they could look out for.

The third weakness are the Prophet predictions, given that the model had very few data points to make a prediction, the predictions can be potentially misleading,
and the user should be informed about their drawbacks.
This could be improved by having a larger timeframe/database or having the data be more granular (weekly, daily), as that would mean 
more data-points to fit the model - usually resulting in a better prediction.
Another method of improvement would be by running multiple models and comparing them, or averaging them, or creating an ensemble model with their 
results, however, the main issue of lack of data would persist throughout, so we might get just more ***wrong*** results
