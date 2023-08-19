import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
# import vaex

import databricks.koalas as ks

# # Read a CSV file into a Koalas DataFrame
# df = ks.read_csv('large_file.csv')

# Load data
airport = pd.read_csv('airports.csv', low_memory=True)
airlines = pd.read_csv('airlines.csv', low_memory=True)
flights = ks.read_csv("flights.csv")
flight=ks.read_csv("flight.csv")
# flight=flight.to_pandas_df()
# flights=flights.to_pandas_df()

# Title and description
# st.title("Flight Delay Prediction")
# st.write("Description: Files, Numerical & Categorical, Missing Values included. Can be used for EDA & Visualization or Prediction")
# st.image("img.jpeg")
# Display the dataset
# if st.checkbox("Show Flights Dataset"):
#     st.subheader("Flights Dataset")
#     st.write(flight.head())

# if st.checkbox("Show Airlines Dataset"):
#     st.subheader("Airlines Dataset")
#     st.write(airlines.head())

# if st.checkbox("Show Airports Dataset"):
#     st.subheader("Airports Dataset")
#     st.write(airport.head())
    
st.sidebar.title("Navigation")

st.sidebar.header("Datasets")
show_flights = st.sidebar.checkbox("Show Flights Dataset")
show_airlines = st.sidebar.checkbox("Show Airlines Dataset")
show_airports = st.sidebar.checkbox("Show Airports Dataset")

    # Proceed with your analysis code here...

st.sidebar.header("Analysis Level")



analysis_level = st.sidebar.selectbox("Select Analysis Level",
                                      ["Project Overview","General Flight Analysis",
                                       "Airport-based Analysis",
                                       "Airline-based Analysis",
                                       "Time-based Analysis"])

if analysis_level == "Project Overview":
    # Main page title and description
    st.title("Flight Delay Prediction Project")
    st.image("img.jpeg")

    # Dataset information
    st.header("About the Dataset")
    st.write("The dataset used for this project is sourced from the U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics.")
    st.write("The dataset includes information on the on-time performance of domestic flights operated by large air carriers.")
    st.write("It provides summary information on the number of on-time, delayed, canceled, and diverted flights.")
    st.write("The dataset covers the year 2015 and focuses on flight delays and cancellations.")

    # Acknowledgments
    st.header("Acknowledgments")
    st.write("The flight delay and cancellation data was collected and published by the DOT's Bureau of Transportation Statistics.")
    st.write("We acknowledge their efforts in collecting and providing this valuable dataset for analysis.")
    # Dataset information
    st.header("Dataset Information")
    st.write("The dataset consists of:")
    st.write("- 5,819,079 flights that took place in the USA in the year 2015.")
    st.write("- 322 airports and 14 airlines.")


    st.header("🤔 Questions we must ask to do Analysis")

    # General Flight Analysis Questions
    st.subheader("General Flight Analysis 🛫")
    st.write("1. How has the total number of flights changed over the years?")
    st.write("2. What is the distribution of cancelled vs. not cancelled flights?")

    # Formatting
    st.markdown("---")

    # Airport-based Analysis Questions
    st.subheader("Airport-based Analysis 🛬")
    st.write("1. What is the geographic distribution of airports?")
    st.write("2. Which are the top origin and destination airports for flights?")
    st.write("3. How do flight numbers vary for each airport launching or receiving flights?")
    st.write("4. Which airports have the most reliable operations?")

    # Formatting
    st.markdown("---")

    # Airline-based Analysis Questions
    st.subheader("Airline-based Analysis ✈️")
    st.write("1. What is the percentage of flights operated by each airline?")
    st.write("2. How many flights has each airline operated?")
    st.write("3. What are the average departure and arrival delays for each airline?")
    st.write("4. Which airline is the most reliable in terms of delay?")

    # Formatting
    st.markdown("---")

    # Time-based Analysis Questions
    st.subheader("Time-based Analysis ⏰")
    st.write("1. How does the distribution of flights vary by time of day?")
    st.write("2. What is the distribution of flights by day of the week?")
    st.write("3. How do flight numbers differ across different seasons?")
    st.write("4. How have delays changed over different time intervals (monthly, weekly, daily)?")
    
    if show_flights:
        st.subheader("Flights Dataset")
        st.write(flight.head(100))

    if show_airlines:
        st.subheader("Airlines Dataset")
        st.write(airlines.head(100))

    if show_airports:
        st.subheader("Airports Dataset")
        st.write(airport.head(100))
    
if analysis_level == "General Flight Analysis":
    st.subheader("General Flight Analysis")

    # Second-level sidebar for sub-analysis options
    sub_analysis = st.sidebar.radio("Select Sub-Analysis",
                                    ["Distribution of Total Flight Numbers",
                                     "Distribution of Cancelled vs. Not Cancelled Flights",
                                     "Most Frequent Tail Numbers Used in 2015"])

    if sub_analysis == "Distribution of Total Flight Numbers":
        st.subheader("Distribution of Total Flight Numbers")
        # Grouping by "YEAR" and calculating the number of flights per year
        flights_per_year = flights.groupby(by=[flights.YEAR]).agg({'FLIGHT_NUMBER': vaex.agg.count()}).to_pandas_df().reset_index()
        # flights_per_year = flights.groupby("YEAR")["FLIGHT_NUMBER"].count().reset_index()

        # Creating the bar chart using Plotly Express
        fig_total_flights = px.bar(flights_per_year, x="YEAR", y="FLIGHT_NUMBER", labels={"FLIGHT_NUMBER": "Number of Flights"}, title="Number of Flights per Year")

        # Show the plot
        st.plotly_chart(fig_total_flights)

    elif sub_analysis == "Distribution of Cancelled vs. Not Cancelled Flights":
        st.subheader("Distribution of Cancelled vs. Not Cancelled Flights")

        # Group by 'CANCELLED' and calculate the counts
        cancelled_counts = flights['CANCELLED'].value_counts().reset_index()
        cancelled_counts.columns = ['Cancelled', 'Count']
        # Create a dictionary to map values to labels
        cancelled_labels = {0: 'Not Cancelled', 1: 'Cancelled'}

        # Replace 'Cancelled' values with labels
        cancelled_counts['Cancelled'] = cancelled_counts['Cancelled'].map(cancelled_labels)
        # Create a bar chart using Plotly Express
        fig_cancelled_vs_not = px.bar(cancelled_counts, x='Cancelled', y='Count', title='Cancelled Flights Distribution',
                    labels={'Cancelled': 'Cancelled', 'Count': 'Number of Flights'})

        # Show the plot
        st.plotly_chart(fig_cancelled_vs_not)

    elif sub_analysis == "Most Frequent Tail Numbers Used in 2015":
        st.subheader("Most Frequent Tail Numbers Used in 2015")
        # top_tail_numbers=flights.groupby(flights.TAIL_NUMBER).agg({'TAIL_NUMBER': vaex.agg.count()}).sort('count', ascending=False).head(10).to_pandas_df()
        top_tail_numbers = flights['TAIL_NUMBER'].value_counts().sort_values(ascending=False).head(10)
        fig_most_frequent_tail = px.bar(x=top_tail_numbers.index, y=top_tail_numbers.values, title='Top 10 Most Frequent Tail Numbers',
                    labels={'x': 'Tail Number', 'y': 'Count'})

        st.plotly_chart(fig_most_frequent_tail)
        
        

elif analysis_level == "Airport-based Analysis":
    st.subheader("Airport-based Analysis")

    # Second-level sidebar for sub-analysis options
    sub_analysis_airport = st.sidebar.radio("Select Airport-based Sub-Analysis",
                                            ["Geo Location of Airports",
                                             "Top 20 Origin Airports for Flights in 2015",
                                             "Top 20 Destination Airports for Flights in 2015",
                                             "Flight Numbers Based on Origin Airport",
                                             "Flight Numbers Based on Destination Airport",
                                             "Flight Numbers Based on Origin Airport and State",
                                             "Flight Numbers Based on Destination Airport and State",
                                             "Most Reliable Airports in 2015"])

    if sub_analysis_airport == "Geo Location of Airports":
        st.subheader("Geo Location of Airports")
        # Plotting the geo location of airports
        fig_airport_map = px.scatter_mapbox(airport,
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        hover_name='AIRPORT',
                        hover_data=['CITY', 'STATE', 'COUNTRY'],
                        zoom=3,
                        title='Airport Locations',
                        mapbox_style='carto-positron'
                       )

        fig_airport_map.update_layout(mapbox=dict(center=dict(lat=37.0902, lon=-95.7129)))  # Set the initial map center (USA)
        st.plotly_chart(fig_airport_map)

    elif sub_analysis_airport == "Top 20 Origin Airports for Flights in 2015":
        st.subheader("Top 20 Origin Airports for Flights in 2015")

        origin_counts = flight['ORIGIN_AIRPORT'].value_counts().reset_index()
        origin_counts.columns = ['Origin Airport', 'Number of Flights']

        # Select the top 20 origin airports
        top_20_origin_counts = origin_counts.head(20)

        # Custom colors for the bars
        colors = px.colors.qualitative.Plotly

        # Creating a bar graph using Plotly Express with custom colors
        fig_top_origin_airports = px.bar(top_20_origin_counts, x='Origin Airport', y='Number of Flights', title='Top 20 Origin Airports by Number of Flights',
                    color='Origin Airport', color_discrete_sequence=colors)

        # Show the graph
        st.plotly_chart(fig_top_origin_airports)

    elif sub_analysis_airport == "Top 20 Destination Airports for Flights in 2015":
        st.subheader("Top 20 Destination Airports for Flights in 2015")

        # Counting the number of flights for each destination airport
        destination_counts = flight['DESTINATION_AIRPORT'].value_counts().reset_index()
        destination_counts.columns = ['Destination Airport', 'Number of Flights']

        # Select the top 20 destination airports
        top_20_destination_counts = destination_counts.head(20)

        # Custom colors for the bars
        colors = px.colors.qualitative.Plotly

        # Creating a bar graph using Plotly Express with custom colors
        fig_top_dest_airports = px.bar(top_20_destination_counts, x="Destination Airport", y='Number of Flights', title='Top 20 Destination Airports by Number of Flights',
                    color='Destination Airport', color_discrete_sequence=colors)
        # Show the graph
        st.plotly_chart(fig_top_dest_airports)

    elif sub_analysis_airport == "Flight Numbers Based on Origin Airport and State":
        st.subheader("Flight Numbers Based on Origin Airport and State")

        # Merge flight data with airport data to include state information
        merged_data = pd.merge(flight, airport, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE', how='left')

        # Calculate the total number of flights originating from each state
        state_counts = merged_data['STATE'].value_counts().reset_index()
        state_counts.columns = ['State', 'Number of Flights']

        # Create a choropleth map using Plotly Express
        fig_origin_flight_counts = px.choropleth(state_counts,
                            locations='State',
                            locationmode='USA-states',
                            color='Number of Flights',
                            color_continuous_scale='Viridis',  # You can choose a different color scale
                            scope='usa',  # Set the scope to the United States
                            title='Flights by Origin Airport and State',
                            labels={'Number of Flights': 'Flight Count'})

        # Show the map
        st.plotly_chart(fig_origin_flight_counts)
    elif sub_analysis_airport == "Flight Numbers Based on Destination Airports and State":
        st.subheader("Flight Numbers Based on Destination Airports and State")
        
        # Merge flight data with airport data to include state information
        merged_data = pd.merge(flight, airport, left_on='DESTINATION_AIRPORT', right_on='IATA_CODE', how='left')

        # Calculate the total number of flights originating from each state
        state_counts = merged_data['STATE'].value_counts().reset_index()
        state_counts.columns = ['State', 'Number of Flights']

        # Create a choropleth map using Plotly Express
        fig_dest_flight_counts = px.choropleth(state_counts,
                            locations='State',
                            locationmode='USA-states',
                            color='Number of Flights',
                            color_continuous_scale='Viridis',  # You can choose a different color scale
                            scope='usa',  # Set the scope to the United States
                            title='Flights by Destination Airport and State',
                            labels={'Number of Flights': 'Flight Count'})

        # Show the map
        st.plotly_chart(fig_dest_flight_counts)
    elif sub_analysis_airport == "Flight Numbers Based on Origin Airport":
        st.subheader("Flight Numbers Based on Origin Airport")

       # Calculate the number of flights for each origin airport
        origin_counts = flight['ORIGIN_AIRPORT'].value_counts().reset_index()
        origin_counts.columns = ['IATA_CODE', 'Number of Flights']

        # Merge origin counts with airport data based on IATA code
        merged_data = pd.merge(origin_counts, airport, on='IATA_CODE', how='inner')

        # Create a scatter plot map using Plotly Express
        fig_origin_state_flight_counts = px.scatter_geo(merged_data,
                            lat='LATITUDE',
                            lon='LONGITUDE',
                            hover_name='AIRPORT',
                            size='Number of Flights',
                            title='Origin Airports and Flight Counts on Map',
                            labels={'Number of Flights': 'Flight Count'},
                            color='Number of Flights')

        # Show the map
        st.plotly_chart(fig_origin_state_flight_counts)

    # Sub-analysis for "Flight Numbers Based on Destination Airport"
    elif sub_analysis_airport == "Flight Numbers Based on Destination Airport":
        st.subheader("Flight Numbers Based on Destination Airport")
        

        # Group flights by destination airport and state and calculate flight counts
        # Calculate the number of flights for each origin airport
        origin_counts = flight['DESTINATION_AIRPORT'].value_counts().reset_index()
        origin_counts.columns = ['IATA_CODE', 'Number of Flights']

        # Merge origin counts with airport data based on IATA code
        merged_data = pd.merge(origin_counts, airport, on='IATA_CODE', how='inner')

        # Create a scatter plot map using Plotly Express
        fig_dest_state_flight_counts = px.scatter_geo(merged_data,
                            lat='LATITUDE',
                            lon='LONGITUDE',
                            hover_name='AIRPORT',
                            size='Number of Flights',
                            title='Destination Airports and Flight Counts on Map',
                            labels={'Number of Flights': 'Flight Count'},
                            color='Number of Flights')

        st.plotly_chart(fig_dest_state_flight_counts)
    elif sub_analysis_airport == "Most Reliable Airports in 2015":
        st.subheader("Most Reliable Airports in 2015")

        # Third-level sidebar for filtering options
        reliability_filter = st.sidebar.radio("Select Reliability Filter",
                                             ["Average Departure Delay",
                                              "Average Arrival Delay",
                                              "Average Total Delay"])

        if reliability_filter == "Average Departure Delay":
            st.subheader("Most Reliable Airports in 2015 (Based on Average Departure Delay)")
            # Calculate average departure delay for each origin airport
            avg_departure_delay_by_origin = flight.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().reset_index()
            avg_departure_delay_by_origin.columns = ['Airport', 'Avg_Departure_Delay']

            # Sort the average departure delay data in ascending order
            sorted_data = avg_departure_delay_by_origin.sort_values(by='Avg_Departure_Delay', ascending=True)

            # Select the top N most reliable airports to show on the graph
            top_airports = 10  # Change this number to select a different number of top airports
            top_airports_df = sorted_data.head(top_airports)

            # Create a bar plot using Plotly
            fig_reliable_dep_delay = px.bar(top_airports_df, x='Avg_Departure_Delay', y='Airport',
                        title=f'Top {top_airports} Most Reliable Airports (Average Departure Delay)',
                        labels={'Avg_Departure_Delay': 'Average Departure Delay', 'Airport': 'Airport Name'})



            st.plotly_chart(fig_reliable_dep_delay)

        elif reliability_filter == "Average Arrival Delay":
            st.subheader("Most Reliable Airports in 2015 (Based on Average Arrival Delay)")
            # Filter flights for the year 2015 and calculate average arrival delay for each airport
            # Calculate average arrival delay for each destination airport
            avg_arrival_delay_by_destination = flight.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].mean().reset_index()
            avg_arrival_delay_by_destination.columns = ['Airport', 'Avg_Arrival_Delay']


            sorted_data = avg_arrival_delay_by_destination.sort_values(by='Avg_Arrival_Delay', ascending=True)

            # Select the top N most reliable destination airports to show on the graph
            top_airports = 10  # Change this number to select a different number of top airports
            top_airports_df = sorted_data.head(top_airports)

            # Create a bar plot using Plotly
            fig_reliable_arr_delay = px.bar(top_airports_df, x='Avg_Arrival_Delay', y='Airport', orientation='h',
                        title=f'Top {top_airports} Most Reliable Destination Airports (Average Arrival Delay)',
                        labels={'Avg_Arrival_Delay': 'Average Arrival Delay', 'AIRPORT': 'Airport Name'})

            # Show the plot
            st.plotly_chart(fig_reliable_arr_delay)

        elif reliability_filter == "Average Total Delay":
            st.subheader("Most Reliable Airports in 2015 (Based on Average Total Delay)")
            # Filter flights for the year 2015 and calculate average total delay for each airport
            # Calculate average departure delay for each origin airport
            avg_departure_delay_by_origin = flight.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().reset_index()
            avg_departure_delay_by_origin.columns = ['Airport', 'Avg_Departure_Delay']

            # Calculate average arrival delay for each destination airport
            avg_arrival_delay_by_destination = flight.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].mean().reset_index()
            avg_arrival_delay_by_destination.columns = ['Airport', 'Avg_Arrival_Delay']

            # Merge the two datasets on the airport code
            reliability_data = pd.merge(avg_departure_delay_by_origin, avg_arrival_delay_by_destination, on='Airport')


            # Calculate the overall reliability measure (you can adjust the formula based on your preference)
            # For example, you can use the sum of inverse delays as a reliability measure
            reliability_data['Reliability'] = 1 / (reliability_data['Avg_Departure_Delay'] + reliability_data['Avg_Arrival_Delay'])

            # Sort the data by reliability measure in descending order
            reliability_data = reliability_data.sort_values(by='Reliability', ascending=False)

            # Select the top N most reliable airports to show on the graph
            top_airports = 7  # Change this number to select a different number of top airports
            top_airports_df = reliability_data.head(top_airports)

            # Create a bar plot using Plotly
            fig_reliable_total_delay = px.bar(top_airports_df, x='Reliability', y='Airport', orientation='h',
                        title=f'Top {top_airports} Most Reliable Airports',
                        labels={'Reliability': 'Reliability Measure', 'AIRPORT': 'Airport Name'})


            
            st.plotly_chart(fig_reliable_total_delay)


elif analysis_level == "Airline-based Analysis":
    st.subheader("Airline-based Analysis")

    # Second-level sidebar for sub-analysis options
    sub_analysis_airline = st.sidebar.radio("Select Airline-based Sub-Analysis",
                                            ["% of Flights by Airline",
                                             "Number of Flights for Each Airline",
                                             "Mean Departure Delay by Airline",
                                             "Mean Arrival Delay by Airline",
                                             "Average Delay by Airline",
                                             "Mean Arrival & Departure Delay by Airline",
                                             "Most Reliable Airline",
                                             "Monthly Flight Delay Analysis",
                                             "Weekly Flight Delay Analysis",
                                             "Daily Flight Delay Analysis",
                                             "Statictical Summary of Airlines"])

    if sub_analysis_airline == "% of Flights by Airline":
        st.subheader("% of Flights by Airline")

        abbr_companies = airlines.set_index('IATA_CODE')['AIRLINE'].to_dict()

        # Subset the DataFrame and redefine the airlines labeling
        df2 = flight.loc[:, ['AIRLINE', 'DEPARTURE_DELAY']]
        df2['AIRLINE'] = df2['AIRLINE'].replace(abbr_companies)

        # Create a list of colors for Plotly using the built-in color palette
        colors = px.colors.qualitative.Prism
        # Create a pie chart for the number of flights per company
        fig_flight_percent_by_airline = px.pie(df2, names='AIRLINE', color_discrete_sequence=colors,
                    title='% of flights per company', hole=0.3)
        fig_flight_percent_by_airline.update_traces(textposition='inside', textinfo='percent+label', customdata=df2['AIRLINE'])

        # # Set the legend: abbreviation -> airline name
        # legend_labels = [abbr_companies[abbr]+ f'({abbr})' for abbr in df2['AIRLINE'].unique()]
        # fig1.update_traces(name=legend_labels)

        st.plotly_chart(fig_flight_percent_by_airline)

    elif sub_analysis_airline == "Number of Flights for Each Airline":
        st.subheader("Number of Flights for Each Airline")

        ## Total Delayed Flights by Airline
        flight_count_per_airline = flight['AIRLINE'].value_counts()

        flight_count_df = flight_count_per_airline.reset_index()
        flight_count_df.columns = ['AIRLINE', 'FlightCount']

        # Merge flight_count_df with airlines_df to get airline names
        combined_df = pd.merge(flight_count_df, airlines, left_on='AIRLINE', right_on='IATA_CODE')

        # Create a bar plot
        fig_flight_counts_by_airline = px.bar(combined_df, x='AIRLINE_y', y='FlightCount', title='Number of Flights by Airline')


        st.plotly_chart(fig_flight_counts_by_airline)

    elif sub_analysis_airline == "Mean Departure Delay by Airline":
        st.subheader("Mean Departure Delay by Airline")

        # calculate the average delay for each airline 
        # CALCULATE THE MEAN TIME DELAY FOR DEPARTURE AND ARRIVAL FOR EACH AIRLINE
        mean_delay_Dep = flight.groupby('AIRLINE')['DEPARTURE_DELAY'].mean()
        mean_delay_Arr= flight.groupby('AIRLINE')['ARRIVAL_DELAY'].mean()

        mean_delay_Dep.sort_values(ascending=False)
        fig_mean_dep_delay_by_airline=px.bar(mean_delay_Dep, x="DEPARTURE_DELAY", y=mean_delay_Dep.index, title='Mean Departure Delay by Airline')

        st.plotly_chart(fig_mean_dep_delay_by_airline)

    elif sub_analysis_airline == "Mean Arrival Delay by Airline":
        st.subheader("Mean Arrival Delay by Airline")
        mean_delay_Arr= flight.groupby('AIRLINE')['ARRIVAL_DELAY'].mean()
        mean_delay_Arr=mean_delay_Arr.sort_values( ascending=False)
        fig_mean_arr_delay_by_airline=px.bar(mean_delay_Arr, x="ARRIVAL_DELAY", y=mean_delay_Arr.index, title='Mean Arrival Delay by Airline')

        st.plotly_chart(fig_mean_arr_delay_by_airline)

    elif sub_analysis_airline == "Average Delay by Airline":
        st.header("Average Delay by Airline")
        # Your avg_delay data
        avg_delay = pd.Series({
            'AA': 12.352228,
            'AS': 0.809238,
            'B6': 18.192213,
            'DL': 7.556008,
            'EV': 15.301313,
            'F9': 25.855565,
            'HA': 2.508806,
            'MQ': 16.583062,
            'NK': 30.416565,
            'OO': 13.646756,
            'UA': 19.867035,
            'US': 9.847346,
            'VX': 13.760301,
            'WN': 14.956950
        })

        # Mapping of airline IATA codes to names
        airline_mapping = {
            'UA': 'United Air Lines Inc.',
            'AA': 'American Airlines Inc.',
            'US': 'US Airways Inc.',
            'F9': 'Frontier Airlines Inc.',
            'B6': 'JetBlue Airways',
            'OO': 'Skywest Airlines Inc.',
            'AS': 'Alaska Airlines Inc.',
            'NK': 'Spirit Air Lines',
            'WN': 'Southwest Airlines Co.',
            'DL': 'Delta Air Lines Inc.',
            'EV': 'Atlantic Southeast Airlines',
            'HA': 'Hawaiian Airlines Inc.',
            'MQ': 'American Eagle Airlines Inc.',
            'VX': 'Virgin America'
        }

        # Create a DataFrame with airline names
        avg_delay_df = pd.DataFrame({'Airline': avg_delay.index, 'AvgDelay': avg_delay.values})
        avg_delay_df['AirlineName'] = avg_delay_df['Airline'].map(airline_mapping)

        # Create a bar plot using Plotly Express
        fig = px.bar(avg_delay_df, x='AvgDelay', y='AirlineName', orientation='h',
                    title='Average Delay by Airline',
                    labels={'AvgDelay': 'Average Delay (min)', 'AirlineName': 'Airline'})

        # Show the plot
        st.plotly_chart(fig)
    elif sub_analysis_airline == "Mean Arrival & Departure Delay by Airline":
        st.header("Mean Arrival & Departure Delay by Airline")
        
        # Calculate the mean delay for each airline
        mean_delay = flight.groupby('AIRLINE')[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()

        # Merge with airlines_df to get full airline names
        combined_df = pd.merge(mean_delay, airlines, left_on='AIRLINE', right_on='IATA_CODE')

        # Create a bar plot
        fig = px.bar(combined_df, x='AIRLINE_y', y=['ARRIVAL_DELAY', 'DEPARTURE_DELAY'],
                    title='Mean Arrival and Departure Delays by Airline',
                    labels={'ARRIVAL_DELAY': 'Mean Arrival Delay', 'DEPARTURE_DELAY': 'Mean Departure Delay'},
                    barmode='group')
        st.plotly_chart(fig)
    elif sub_analysis_airline == "Most Reliable Airline":
        st.subheader("Most Reliable Airline")

        # Calculate average arrival and departure delay for each airline
        airline_stats = flights.groupby('AIRLINE').agg({
            'ARRIVAL_DELAY': 'mean',
            'DEPARTURE_DELAY': 'mean'
        }).reset_index()

        # Merge with airlines_df to get full airline names
        airline_stats = pd.merge(airline_stats, airlines, left_on='AIRLINE', right_on='IATA_CODE')

        # Sort by average arrival delay for better visualization
        airline_stats = airline_stats.sort_values(by='ARRIVAL_DELAY')

        # Create a grouped bar chart
        fig = go.Figure(data=[
            go.Bar(name='Average Arrival Delay', x=airline_stats['AIRLINE_y'], y=airline_stats['ARRIVAL_DELAY']),
            go.Bar(name='Average Departure Delay', x=airline_stats['AIRLINE_y'], y=airline_stats['DEPARTURE_DELAY'])
        ])

        # Update layout
        fig.update_layout(barmode='group',
                        title='Average Arrival and Departure Delay by Airline',
                        xaxis_title='Airline',
                        yaxis_title='Delay',
                        legend_title='Delay Type')

        # Show the plot
        st.plotly_chart(fig)
        
    elif sub_analysis_airline == "Monthly Flight Delay Analysis":
        st.header("Monthly Flight Delay Analysis")
        # Convert date columns to datetime format
        flight['SCHEDULED_DEPARTURE'] = pd.to_datetime(flight['SCHEDULED_DEPARTURE'])

        # Extract year and month
        flight['Year'] = flight['SCHEDULED_DEPARTURE'].dt.year
        flight['Month'] = flight['SCHEDULED_DEPARTURE'].dt.month

        # Calculate mean delay for each airline for each month
        mean_monthly_delay = flight.groupby(['Year', 'Month', 'AIRLINE'])[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()

        # Merge with airlines_df to get full airline names
        combined_df = pd.merge(mean_monthly_delay, airlines, left_on='AIRLINE', right_on='IATA_CODE')

        # Create a line plot to visualize monthly flight delays
        fig = px.line(combined_df, x='Month', y=['ARRIVAL_DELAY', 'DEPARTURE_DELAY'],
                    color='AIRLINE_x',  # Use 'AIRLINE_x' column as color grouping
                    labels={'Month': 'Month', 'value': 'Mean Delay'},
                    title='Monthly Flight Delays by Airline',
                    line_group='AIRLINE_y')  # Use 'AIRLINE_x' column as line grouping
        fig.update_xaxes(type='category')
        # Calculate mean delay for each airline for each month
        mean_monthly_delay = flight.groupby(['Year', 'Month', 'AIRLINE'])[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()
        combined_df = pd.merge(mean_monthly_delay, airlines, left_on='AIRLINE', right_on='IATA_CODE')
        # Create a scatter plot with trend lines using Plotly
        fig1 = px.scatter(combined_df, x='Month', y='ARRIVAL_DELAY', title='Monthly Mean Flight Time Delay Trend (All Airlines)',
                        labels={'Month': 'Month', 'ARRIVAL_DELAY': 'Mean Arrival Delay'},hover_name="AIRLINE_y"
                        )

        # Set x-axis tick labels
        fig1.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        # Calculate mean delay for each airline for each month
        mean_monthly_delay = flight.groupby(['Year', 'Month'])[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()

        # Create a line plot with trend lines using Plotly
        fig2 = px.line(mean_monthly_delay, x='Month', y='ARRIVAL_DELAY', title='Monthly Mean Flight Arrival Delay Trend (All Airlines)',
                    labels={'Month': 'Month', 'ARRIVAL_DELAY': 'Mean Arrival Delay'})

        # Set x-axis tick labels
        fig2.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

        

        # Calculate mean delay for each airline for each month
        mean_monthly_delay = flight.groupby(['Year', 'Month'])[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()

        # Create a line plot using Plotly
        fig3 = px.line(mean_monthly_delay, x='Month', y='DEPARTURE_DELAY', title='Monthly Mean Flight Departure Delay Trend (All Airlines)',
                    labels={'Month': 'Month', 'DEPARTURE_DELAY': 'Mean Departure Delay'})

        # Set x-axis tick labels
        fig3.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

        # Show the plot
        st.plotly_chart(fig)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
    elif sub_analysis_airline == "Weekly Flight Delay Analysis":
        st.header("Weekly Flight Delay Analysis")
         # Convert date columns to datetime format
        flight['SCHEDULED_DEPARTURE'] = pd.to_datetime(flight['SCHEDULED_DEPARTURE'])
        # Extract year and week
        flight['Year'] = flight['SCHEDULED_DEPARTURE'].dt.year
        flight['Week'] = (flight['SCHEDULED_DEPARTURE'].dt.strftime('%U'))
        mean_weekly_delay = flight.groupby(['Year', 'Week', 'AIRLINE'])[['ARRIVAL_DELAY','DEPARTURE_DELAY']].mean().reset_index()

        # Merge with airlines_df to get full airline names
        combined_df = pd.merge(mean_weekly_delay, airlines, left_on='AIRLINE', right_on='IATA_CODE')
        # Create scatter plot with trendline using Plotly Express
        fig = px.scatter(combined_df,
                        x='Week',
                        y='ARRIVAL_DELAY',
                        title='Weekly Flight Arrival Delays with Trend Line',
                        hover_name='AIRLINE_y',
                        labels={'Week': 'Week', 'ARRIVAL_DELAY': 'Mean Arrival Delay'},
                        )  

        # Show the plot

        # Merge with airlines_df to get full airline names
        combined_df = pd.merge(mean_weekly_delay, airlines, left_on='AIRLINE', right_on='IATA_CODE')
        # Create scatter plot with trendline using Plotly Express
        fig1 = px.scatter(combined_df,
                        x='Week',
                        y='DEPARTURE_DELAY',
                        title='Weekly Flight Departure Delays with Trend Line',
                        hover_name='AIRLINE_y',
                        labels={'Week': 'Week', 'DEPARTURE_DELAY': 'Mean DEPARTURE DELAY '},
        )

        # Show the plot
        # Calculate mean arrival delay for each week
        mean_weekly_delay = flight.groupby(['Year', 'Week'])[['ARRIVAL_DELAY',"DEPARTURE_DELAY"]].mean().reset_index()

        # Create scatter plot with trendline using Plotly Express
        fig2 = px.line(mean_weekly_delay,
                        x='Week',
                        y='ARRIVAL_DELAY',
                        title='Weekly Mean Flight Arrival Delay with Trend Line',
                        labels={'Week': 'Week', 'ARRIVAL_DELAY': 'Mean Arrival Delay'},
                        )

        # Show the plot
        # Calculate mean arrival delay for each week
        mean_weekly_delay = flight.groupby(['Year', 'Week'])[['ARRIVAL_DELAY',"DEPARTURE_DELAY"]].mean().reset_index()

        # Create scatter plot with trendline using Plotly Express
        fig3 = px.line(mean_weekly_delay,
                        x='Week',
                        y='DEPARTURE_DELAY',
                        title='Weekly Mean Flight Departure Delay with Trend Line',
                        labels={'Week': 'Week', 'DEPARTURE_DELAY': 'Mean Departure Delay'},
                        )

        # Show the plot
        # Calculate mean arrival and departure delay for each week
        mean_weekly_delay = flight.groupby(['Year', 'Week'])[['ARRIVAL_DELAY', 'DEPARTURE_DELAY']].mean().reset_index()

        # Calculate combined delay (arrival delay + departure delay)
        mean_weekly_delay['COMBINED_DELAY'] = mean_weekly_delay['ARRIVAL_DELAY'] + mean_weekly_delay['DEPARTURE_DELAY']

        # Create line plot using Plotly Express
        fig4 = px.line(mean_weekly_delay,
                    x='Week',
                    y=['ARRIVAL_DELAY', 'DEPARTURE_DELAY'],
                    title='Weekly Mean Flight Combined Delay (Departure Delay + Arrival Delay) with Trend Line',
                    labels={'Week': 'Week', 'COMBINED_DELAY': 'Mean Combined Delay'},
                    )

        # Show the plot
        st.plotly_chart(fig)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
    elif sub_analysis_airline == "Daily Flight Delay Analysis":
        st.header("Daily Flight Delay Analysis")
        flight['SCHEDULED_DEPARTURE'] = pd.to_datetime(flight['SCHEDULED_DEPARTURE'], format='%Y-%m-%d %H:%M:%S')

        # Extract the day of the week and create a new column 'DAY_OF_WEEK'
        flight['DAY_OF_WEEK'] = flight['SCHEDULED_DEPARTURE'].dt.day_name()


        # Group flights by day of the week and calculate the average departure delay
        daily_delay_by_day = flight.groupby('DAY_OF_WEEK')['DEPARTURE_DELAY'].mean().reset_index()

        # Specify the desired order of days
        desired_day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create a bar plot
        bar_fig = px.bar(daily_delay_by_day, x='DAY_OF_WEEK', y='DEPARTURE_DELAY', title='Average Departure Delay by Day of the Week',
                        labels={'DAY_OF_WEEK': 'Day of the Week', 'DEPARTURE_DELAY': 'Average Departure Delay'},
                        category_orders={'DAY_OF_WEEK': desired_day_order})  # Set the desired order

       
        # Group flights by day of the week and calculate the average departure delay
        daily_delay_by_day_ARR = flight.groupby('DAY_OF_WEEK')['ARRIVAL_DELAY'].mean().reset_index()

        # Specify the desired order of days
        desired_day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create a bar plot
        bar_fig1 = px.bar(daily_delay_by_day_ARR, x='DAY_OF_WEEK', y='ARRIVAL_DELAY', title='Average ARRIVAL Delay by Day of the Week',
                        labels={'DAY_OF_WEEK': 'Day of the Week', 'ARRIVAL_DELAY': 'Average ARRIVAL Delay'},
                        category_orders={'DAY_OF_WEEK': desired_day_order})  # Set the desired order



        # Group flights by day of the week and calculate the average departure and arrival delays
        daily_delay_by_day = flight.groupby('DAY_OF_WEEK')[['DEPARTURE_DELAY', 'ARRIVAL_DELAY']].mean().reset_index()

        # Specify the desired order of days
        desired_day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create a bar plot
        bar_fig2 = px.bar(daily_delay_by_day, x='DAY_OF_WEEK', y=['DEPARTURE_DELAY', 'ARRIVAL_DELAY'],
                        title='Average Departure and Arrival Delays by Day of the Week',
                        labels={'DAY_OF_WEEK': 'Day of the Week', 'value': 'Average Delay'},
                        category_orders={'DAY_OF_WEEK': desired_day_order},  # Set the desired order
                        color_discrete_map={'DEPARTURE_DELAY': 'blue', 'ARRIVAL_DELAY': 'orange'},  # Assign colors to delays
                        barmode='group')  # Grouped bar plot
        st.plotly_chart(bar_fig)
        st.plotly_chart(bar_fig1)
        st.plotly_chart(bar_fig2)

        
        
    elif sub_analysis_airline == "Statictical Summary of Airlines":
        st.header("Statictical Summary of Airlines")
        # function that extract statistical parameters from a grouby objet:
        def get_stats(group):
            return {'min': group.min(), 'max': group.max(),
                    'count': group.count(), 'mean': group.mean()}
        global_stats = flight['DEPARTURE_DELAY'].groupby(flight['AIRLINE']).apply(get_stats).unstack()
        global_stats = global_stats.sort_values('count')
        st.write(global_stats)
        fig_stats = px.bar(global_stats,
                   x=global_stats.index,
                   y=['min', 'max', 'count', 'mean'],
                   title='Statistical Summary of Airlines',
                   labels={'x': 'Airline', 'value': 'Value', 'variable': 'Statistic'},
                   barmode='group')

        # Show the plot
        st.plotly_chart(fig_stats)

        


elif analysis_level == "Time-based Analysis":
    st.subheader("Time-based Analysis")

    # Checkbox for "Distribution of Flights by Time of Day" sub-analysis
    sub_analysis_time_of_day = st.sidebar.checkbox("Distribution of Flights by Time of Day")

    # Checkbox for "Distribution of Flights by Day of Week" sub-analysis
    sub_analysis_day_of_week = st.sidebar.checkbox("Distribution of Flights by Day of Week")

    # Checkbox for "Distribution of Flights by Season" sub-analysis
    sub_analysis_season = st.sidebar.checkbox("Distribution of Flights by Season")

    if sub_analysis_time_of_day:
        st.subheader("Distribution of Flights by Time of Day")
        # Extract hour from 'SCHEDULED_DEPARTURE'
        flight['DEPARTURE_HOUR'] = pd.to_datetime(flight['SCHEDULED_DEPARTURE']).dt.hour

        # Define a function to map hours to time of day labels
        def map_hour_to_time_of_day(hour):
            if 5 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 21:
                return 'Evening'
            else:
                return 'Night'

        # Apply the function to create a new column 'TIME_OF_DAY'
        flight['TIME_OF_DAY'] = flight['DEPARTURE_HOUR'].apply(map_hour_to_time_of_day)

        # Grouping data by time of day and calculating the number of flights
        time_of_day_flight_counts = flight.groupby('TIME_OF_DAY')['AIRLINE'].count().reset_index()


        # Creating a bar plot using Plotly Express
        fig_time_of_day_flight_counts = px.bar(time_of_day_flight_counts,
                    x='TIME_OF_DAY',
                    y='AIRLINE',
                    labels={'TIME_OF_DAY': 'Time of Day', 'AIRLINE': 'Number of Flights'},
                    title='Distribution of Flights by Time of Day',
                    category_orders={"TIME_OF_DAY": ["Morning", "Afternoon", "Evening", "Night"]})
        st.plotly_chart(fig_time_of_day_flight_counts)

        if sub_analysis_day_of_week:
            st.subheader("Distribution of Flights by Day of Week")

            # Group the data by the 'DAY_OF_flight' and calculate the flight count for each day
            flight_count_by_day_of_week = flight.groupby('DAY_OF_WEEK').size().reset_index(name='FLIGHT_COUNT')

            # Sort the data by the 'FLIGHT_COUNT' column in descending order
            flight_count_by_day_of_week = flight_count_by_day_of_week.sort_values(by='FLIGHT_COUNT', ascending=False)

            # Sort the day of the week in the desired order (Monday to Sunday)
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            flight_count_by_day_of_week['DAY_OF_WEEK'] = pd.Categorical(flight_count_by_day_of_week['DAY_OF_WEEK'], categories=day_order, ordered=True)

            # Create a bar chart using Plotly
            fig_flight_count_by_day_of_week = px.bar(flight_count_by_day_of_week, x='DAY_OF_WEEK', y='FLIGHT_COUNT',
                        title='Number of Flights by Day of the Week (Sorted by Flight Count)',
                        labels={'DAY_OF_WEEK': 'Day of Week', 'FLIGHT_COUNT': 'Number of Flights'})
            st.plotly_chart(fig_flight_count_by_day_of_week)

        if sub_analysis_season:
            st.subheader("Distribution of Flights by Season")

            flight['SCHEDULED_DEPARTURE'] = pd.to_datetime(flight['SCHEDULED_DEPARTURE'], format='%Y-%m-%d %H:%M:%S')

            def get_season(dt):
                if dt.month in [12, 1, 2]:
                    return 'Winter'
                elif dt.month in [3, 4, 5]:
                    return 'Spring'
                elif dt.month in [6, 7, 8]:
                    return 'Summer'
                else:
                    return 'Fall'

            flight['SEASON'] = flight['SCHEDULED_DEPARTURE'].apply(get_season)

            flight_count_by_season = flight.groupby('SEASON').size().reset_index(name='FLIGHT_COUNT')
            print(flight_count_by_season)

            flight_count_by_season_sorted = flight_count_by_season.sort_values(by='FLIGHT_COUNT', ascending=False)
            # Create a bar chart using Plotly
            fig_flight_count_by_season = px.bar(flight_count_by_season_sorted, x='SEASON', y='FLIGHT_COUNT',
                        title='Number of Flights by Season',
                        labels={'SEASON': 'Season', 'FLIGHT_COUNT': 'Number of Flights'},)
            st.plotly_chart(fig_flight_count_by_season)
            





# # Display the pie chart and strip plot
# if analysis_level == "Airline-based Analysis":
#     st.subheader("Pie Chart: Mean delay at origin")
#     st.plotly_chart(fig2)

#     st.subheader("Strip Plot: Departure delay")
#     st.plotly_chart(fig3)



