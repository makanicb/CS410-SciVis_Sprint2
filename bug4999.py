OpenDatabase("/home/users/makanib/uoregon-cs410-scivis/sprint2/KelvinHelmholtz/pyranda.visit") 
AddPlot("Pseudocolor", "rho", 1, 1)
DrawPlots()
for i in range(3):
    Query("Time")
    print("Time %d: %s" %(i , GetQueryOutputValue()))
    TimeSliderNextState()
