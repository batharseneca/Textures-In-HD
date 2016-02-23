from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.palettes import Greys9
import numpy

# Pandas Magic



blue = numpy.load("screen.npy")



Greys9 = list(reversed(Greys9))



output_file("image.html", title="image.py example")

p = figure(x_range=[0, 255], y_range=[0, 255])
p.image(image=[blue], x=[0], y=[0], dw=[255], dh=[255], palette=Greys9)

show(p)  # open a browser