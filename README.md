# VEHICLE ROUTING PROBLEM WITH TIME WINDOWS

Vehicle Routing Problem With Time Windows (VRPTW) Can Be Defined As Choosing Routes For Limited Number Of Vehicles To Serve A Group Of Customers In The Time Windows. Each Vehicle Has A Limited Capacity. It Starts From The Depot And Terminates At The Depot. Each Customer Should Be Served Exactly Once.

# Requirements:
-	Modules
	 - pip install pandas
	 - pip install django
	 - pip install sklearn
	 - pip install mpu
	 - pip install keyboard

# Functions Definitons:

- remove_location :- remove perticular row from dataframe
- distance_time :- calculate distance from two latitude and longitude
- routing :- calculate matrix of route and define best path to traverse through best path
- routing :- 
	Create best path:- 

	All the locations are first clustered using KMeans clustering keeping the number of clusters as `total_locations/10` where 10 represents the maximum working hours of one technician. 
	Each cluster thus formed represents the zone of a particular technician, and every point(representing a client) of the cluster must be attended in a day.
	Sequence for the technician is calculated by fixing a starting point in the cluster and iterating through the shortest point subsequently. So, if the technician starts from a position 'A', the next service location will be the one closest to 'A', say 'B'. Now the next service location will be the one closest to 'B', say 'C' and so on.
	
-	For emergency case:

	 While working hours counting, you can add your urgent case which disrectly add to perticular worker list to their next destination.
	 Steps to add:-
	 		1. press space bar to pause loop.
			2. enter latitude and longitude
			3. press enter

- get_area :- gives the area name from latitude and longitude values

- How To Run:- 

1. Set dataframe location
2. Run - This will display list of workers and working hours


