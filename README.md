Travel companion app

API Endpoints:
- '/': Main page, where user sees all their trips if logged in. Not, redirects to login page.
- '/login': Login endpoint
- '/logout': Logs user out and redirects to login page
- '/register': Registration endpoint
- '/trip/<trip_id>': To see details of a specific trip.
- '/trip-create': Create a new trip
- '/trip-update/<trip_id>': Modify details of the trip with specified id.
- '/trip-delete/<trip_id>': Delete specified trip from the list
- 'city-create/<trip_id>': Add a new destination city to the existing trip.
- 'city-update/<trip_id>': Modify details of the city for the trip with specified id.
- 'city-delete/<trip_id>': Delete the city for the trip with specified id.
