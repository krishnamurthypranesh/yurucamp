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
<img width="655" alt="tlg_sequence_diagram" src="https://github.com/krishnamurthypranesh/yurucamp/assets/30997905/b66b3e07-1ba5-49f7-ba92-8d8074c2246f">
