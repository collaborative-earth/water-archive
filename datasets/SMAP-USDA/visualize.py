from bokeh.io import output_notebook 
from bokeh.plotting import figure, output_file, show 
from bokeh.palettes import brewer, colorblind
import ee
import folium
from water_common import bboxes
from IPython.display import Image

_ = output_notebook()

# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name = name,
    overlay = True,
    control = True
  ).add_to(self)


# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer


def legend(
        palette: tuple,
        title: str='Legend Title (-)',
        plot_width: int=500,
        plot_height: int=75,
        minimum: float=0,
        maximum: float=1):
    pal_len = len(palette)
    pal_dist = maximum - minimum
    width_color = pal_dist/pal_len
    x_locs = [minimum + .5 * width_color * ((2 * ii) - 1)
              for ii in range(pal_len+1) if ii != 0]
    # print(width_color)
    # print(x_locs)

    legend = figure(
        title=title, 
        plot_width=plot_width, 
        plot_height=plot_height)
    
    _ =legend.vbar(
        x = x_locs,  
        top = [0] * pal_len, 
        bottom = [1] * pal_len, 
        width = width_color, 
        color = palette) 
    show(legend)
    return None


# hmpf, no real gain
def folium_map(**kwargs):
    folium_map = folium.Map(**kwargs)
    return folium_map


def folium_display(the_map):
    the_map.add_child(folium.LayerControl())
    display(the_map)
    return None


def img_range(
        img,
        area_of_interest=None,
        scale_m: int=.1):

    if area_of_interest is None:
        area_of_interest = bboxes()['world']

    min = (img
           .reduceRegion(
               ee.Reducer.min(), area_of_interest, bestEffort=True)
           .values().getInfo())
    max = (img
           .reduceRegion(
               ee.Reducer.max(), area_of_interest, bestEffort=True)
           .values().getInfo())

    # probably not the best way to handle this
    if len(min) > 1 or len(max) > 1:
        raise ValueError('Passed image has multiple bands')
        
    return [min[0], max[0]]


def img_col_range(
        img_col,
        area_of_interest=None,
        scale_m: int=.1):

    if area_of_interest is None:
        area_of_interest = bboxes()['world']

    min = img_range(img_col.min(), area_of_interest, scale_m)[0]
    max = img_range(img_col.max(), area_of_interest, scale_m)[1]

    return [min, max]


