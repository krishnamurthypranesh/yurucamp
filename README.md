# Intro
A simple holiday planner that lets users plan their holidays by checking the weather at the location of their choice

# Problem Statement
A company is building a holiday planner. Customers can choose a sequence of destinations as a schedule, taking the weather at each location into account.
Your task is to implement an API which could be used by a frontend (note: don’t write a front-end) to enable this functionality.

# Research

- To figure out a good user experience, I trialed the following products:
    - [Triptile](https://triptile.com/)
    - [Wanderlog](https://wanderlog.com/home)

### Triptile

- The experience on triptile was fairly straight-forward:
- A user lands on their website
- Selects a bunch of places
- Decides how long they want to stay in a particular place
- After this point, the platform gives them an estimated cost and suggests hotels, restaurants and places to visit based off this
- They user can choose to save this information. But, they need to be logged in

### Wanderlog

- The experience is slightly different (and slightly more complicated)
- The user has to be logged in to use the webapp
- Once logged in, the user can start a new plan (this will be saved as draft by default)
- Then, the user is redirected to a different page where:
    - They can choose places from a search bar
    - Or from a list of pre-determined suggestions
- Each time they choose a place, its shown on a map widget on the right
- After selecting their places, the user can choose to plan out the rest of the components of the trip

### Conclusion

- I personally liked triptile’s implementation better:
    - Since it was very straight-forward
    - Offered a good suggestion of places

I will be implementing something similar (but much simpler)

# My Implementation

- My focus was to implement only the set of endpoints required to enable the flow where the user:
    - Chooses locations
    - Checks the weather
    - Save the itinerary
- Things I have not implemented:
    - User authentication and authorization
    - Behavior for editing/deleting an already created trip
# Figures and Charts
## Sequence Diagram
<img width="655" alt="tlg_sequence_diagram" src="https://github.com/krishnamurthypranesh/yurucamp/assets/30997905/b66b3e07-1ba5-49f7-ba92-8d8074c2246f">

## Data Model
<img width="616" alt="tlg_data_model" src="https://github.com/krishnamurthypranesh/yurucamp/assets/30997905/5a3fc034-9ef8-42e4-b8f7-5bc3a5421697">

# Limitations and Improvements
## Bugs
### GET /v1/trips/locations
- No major bugs

### GET /v1/trips/weather-check
- Open-meteo the service used to check the weather at a particular place, allows dates that are less than 14 days in the future only
- As a continuation of the previous bug, errors are not handled correctly. Irrespective of what the issue is, the API always returns a 500
- All time data dealt with is treated as naive-date only. This is an issue that can potentially cause problems for the user when they move across timezones
[The assumption here is that the timezone normalization to UTC will be handled by the frontend client and the backend API will get datetimes with a timezone offset of `00:00`
- When a user selects a location, they will select two dates: a start date and an end date. The API only accepts the start date and assumes that displaying weather information for +/-  1 day will suffice

### POST /v1/trips
- Timezones aren’t handled
- Validation of the trip JSON doesn’t validate that `start_date < end_date` for the individual locations
- Improper handling of the draft status of the trip
- Lack of validation of the locations supplied. There are multiple problems with this particular bug:
    - The locations JSON that’s saved doesn’t use `city_code` or `country_code` and instead accepts two random string fields without proper validation
    - The locations are not checked to verify if the system currently supports the locations. Only the structure of the JSON object supplied is validated

## Improvements
- Since I was short on time, I have written only integration tests for the system that test for the behaviour of endpoints and not individual pieces of logic
- I have not added any global logging and have defaulted to using module-level loggers. So, configuring a global logger will improve observability
- No global error handling. Errors are currently handled in the respective code that runs. Instead, a better way to do this would be to add middleware that automatically catches errors and returns the appropriate response based on the exception caught.
- More documentation: Since the implementation itself is simple, I have not added any docstrings, or top-level documentation explaining the logic. This is another definite point of improvement

# Items Currently Work in Progress
- Tests for authentication module

# Completed
- [X] Custom authentication module (sans tests)
