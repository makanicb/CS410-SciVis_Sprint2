OpenDatabase("/home/users/makanib/uoregon-cs410-scivis/sprint2/multi_rect3d.silo")

AddPlot("Pseudocolor", "d")

DrawPlots()

Query("MinMax")

DefineScalarExpression("grad_mag", "magnitude(gradient(d))")
AddPlot("Pseudocolor", "grad_mag")
DrawPlots()
Query("MinMax")

print(GetQueryOutputString())

