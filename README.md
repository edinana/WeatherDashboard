**Weather Dashboard**

**Overview**

The Weather Dashboard is a full-stack web application built using Django, which combines both the frontend and backend in one place for easy management and scalability. The application retrieves current weather data from multiple sources, processes and combines it, and then provides users with real-time weather information, historical data predictions, and forecasts. It uses a Postgres database to store hourly historical data for the past 4 years (2021-2024), which is leveraged for prediction purposes.

**Key Features**

1. Real-time Weather Data: The dashboard fetches current weather data from multiple sources:

    a. OpenWeatherMap
   
    b. WeatherStack
   
    c. WeatherBit
   
    The data is combined using weighted averages and medians to avoid outliers, especially when values differ by more than 5%.

2. Data Caching: Current weather data is cached in Redis for 1 hour to reduce API calls and improve performance.

3. Historical Data: The database stores hourly historical weather data from OpenMeteo (since it's open-source) for the past 4 years. This data is used for prediction purposes, specifically when creating forecasts based on historical weather patterns.

4. Forecast Predictions:

    a. When a user selects a city and presses the forecast button, the application generates a vector with current weather parameters (temperature, condition, humidity, wind speed).
   
    b. Historical data from the same day and hour over the past 4 years, along with data from the past and future 5 days, is retrieved.
   
    c. Cosine Similarity is performed between the current weather vector and historical data vectors to predict the next hour’s weather based on historical trends.
   
    d. For categorical data (e.g., weather condition), the majority value is selected using count-based voting.

5. City Selection: Users can choose a city from a dropdown menu of capitals only.

**Data Sources**

1. Weather Data: The current weather data is fetched from the following APIs:

    a. OpenWeatherMap
   
    b. WeatherStack
   
    c. WeatherBit
   
    Data from these sources is combined into a single report. For numerical values (temperature, humidity, wind speed), weighted averages and medians are calculated. If the values differ by more than 5%, the median value is used to avoid the effect of outliers.

2. Historical Data: Hourly historical weather data for the past 4 years (2021-2024) is stored in a Postgres database. Data is retrieved from OpenMeteo, as it is an open-source option.

**Architecture**

1. Django: Used for both the backend and frontend, making it easy to manage and scale the application.

2. Postgres: Stores historical weather data for the past 4 years (2021-2024), which is used for predictions.

3. Redis: Caches the current weather data for 1 hour to minimize API calls.

4. Facade Design Pattern: Different weather data sources can be added easily using the facade design pattern, allowing for flexibility and extensibility in adding new data providers.

**Improvements**
1. Scheduler for Weather Updates: Implement a scheduler to periodically pull current weather data and save it to the database.
   
2. Use Recent Data for Predictions: Incorporate the past 3 hours of weather data into the prediction model.
   
3. Cache Management: Use a scheduler (e.g., Celery) to clear the Redis cache at the beginning of every hour, ensuring that new data is fetched.
   
4. Additional Parameters: Include more parameters, such as atmospheric pressure or cloud cover, in the prediction logic.
   
5. Dynamic Confidence Scores: Adjust the confidence scores for each weather source based on their performance and accuracy over time.
   
**Limitations**
1. OpenMeteo Historical Data: The historical data provided by OpenMeteo does not always offer high accuracy, but it was the best available open-source option.
2. WeatherStack Usage Limits: WeatherStack was temporarily blocked due to exceeding the monthly usage limit. An upgrade is required to continue using the service.

**Screenshots**

Current Weather Display
![image](https://github.com/user-attachments/assets/5745e933-aef3-4212-acb4-3c43a64f09e6)

Predicted Weather Display
![image](https://github.com/user-attachments/assets/47a480ff-14b7-41e7-97ea-79c7026807bf)
