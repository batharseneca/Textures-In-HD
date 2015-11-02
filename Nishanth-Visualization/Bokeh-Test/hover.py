from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool, PanTool, ResizeTool
import pandas as pd
import seaborn as sns
import sys
from collections import OrderedDict

## Using a sample Dataset (PCA from 1000 genomes project), created a interactive plotting function


# Reads in the files
file1 = 'C:\\Users\\Nishanth\\Documents\\PythonScripts\\plink.eigenvec'
PCA = pd.read_table(file1,sep=" ",dtype=None)
file2 = 'C:\\Users\\Nishanth\\Documents\\PythonScripts\\HGDPid.csv'
meta = pd.read_table(file2,sep=",",dtype=None)


# Renames ID column and merges PCA and metadata on PCA
meta.columns = ('FID','Sex','poulation','geographic_origin','region','pop7groups')
merged = PCA.merge(meta,how='inner',on='FID')



output_file("toolbar.html")

source = ColumnDataSource(merged)

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"	

p = figure(plot_width=1200, plot_height=800, tools=TOOLS,
           title="1000 Genomes according to Population Group")

		   
hover = p.select(dict(type=HoverTool))
hover.point_policy = "follow_mouse"
hover.tooltips = OrderedDict([
    ("FID", "@FID"),
    ("(PC1,PC2)", "(@PC1, @PC2)"),
    ("Population Group", "@pop7groups"),
])

import seaborn as sns

palette = (sns.color_palette("husl", len(set(merged["pop7groups"]))).as_hex())


# Converts to Series
palette = pd.Series(list(palette))
groups = pd.Series(list(set(merged["pop7groups"])))

# Creates a palette DF
palDF = pd.DataFrame(palette)
palDF["pop7groups"] = groups
palDF.columns = ["palette","pop7groups"]

# Merges the two together
merged = merged.merge(palDF,how="inner",on="pop7groups")

# print(merged.ix[:,["pop7groups","palette"]])

p.circle("PC1","PC2",fill_alpha=1,size=10,line_alpha=0,source=source,color=merged["palette"])

show(p)






