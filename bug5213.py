# test_bg_fg_color.py
OpenDatabase("/home/users/makanib/uoregon-cs410-scivis/proj6/test.makani")
AddPlot('Mesh', 'main')
DrawPlots()

# Get the annotation attributes (this controls bg/fg color in VisIt)
annot = GetAnnotationAttributes()

# Set background color (RGBA)
annot.backgroundColor = (0, 0, 0, 255)      # black
annot.foregroundColor = (255, 255, 255, 255) # white
annot.backgroundMode = annot.Solid           # vs Gradient, Image, etc.

SetAnnotationAttributes(annot)

print("backgroundColor:", annot.backgroundColor)
print("foregroundColor:", annot.foregroundColor)


