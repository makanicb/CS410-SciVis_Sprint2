OpenDatabase("/home/users/makanib/visit3.4.0/build/bin/overlinkMatColorsNullMatnames/OvlTop.silo")
print("AddPlot()")
AddPlot("FilledBoundary", "MMATERIAL")
print("DrawPlots()")
DrawPlots()

# Get the plot attributes to see what materials VisIt registered
print("FilledBoundaryAttributes()")
a = FilledBoundaryAttributes()
print(a)

# See what variables VisIt actually found in the file
print("GetMetaData()")
md = GetMetaData("overlinkMatColorsNullMatnames/OvlTop.silo")
print(md)

# Query the spatial extents of the full plot
Query("SpatialExtents")
print("Full spatial extents:", GetQueryOutputValue())
