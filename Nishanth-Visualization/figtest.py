from bokeh.models import ColumnDataSource, OpenURL, TapTool
from bokeh.plotting import figure, output_file, show

output_file("openurl.html")

p = figure(plot_width=1200, plot_height=1200,
           tools="tap", title="Click the Dots")

		   
		   
file = 'C:\\Users\\Nishanth\\Documents\\PythonScripts\\plink.eigenvec'
PCA = np.genfromtxt(file,delimiter=" ",dtype=None, names=True)
file = 'C:\\Users\\Nishanth\\Documents\\PythonScripts\\HGDPid.csv'
meta = np.genfromtxt(file,delimiter=",",dtype=None, names = True)

		   
		   
		   

		   
source = columnDataSource(data=)


ColumnDataSource(data=dict(
    x=[1, 2, 3, 4, 5],
    y=[2, 5, 8, 2, 7],
    color=["navy", "orange", "olive", "firebrick", "gold"]
    ))

p.circle('x', 'y', color='color', size=2, source=source)

url = "http://www.colors.commutercreative.com/@color/"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

show(p)