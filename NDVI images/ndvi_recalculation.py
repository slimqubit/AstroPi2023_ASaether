### Packages
from PIL import Image
import cv2
import numpy 
import numpy as np
from numpy import uint8
import matplotlib.pyplot as plt

### Packages for ColorMaps (interpreting the images)
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors



### Function that displays image
#def display_toconsole(image, image_name):
#    image = np.array(image, dtype=float)/float(255) # convert to an array
#    shape = image.shape # change shape
#    height = int(shape[0]/2)
#    width = int(shape[1]/2)
#    image = cv2.resize(image, (width, height)) # resize image
#    cv2.namedWindow(image_name) # create window
#    cv2.imshow(image_name, image) # display image
#    cv2.waitKey(0) # wait for key press
#    cv2.destroyAllWindows()


### Function that stretches the contrast of images to minimum (0) and maximum (255)
def constrast_stretch(image):
    in_min = np.percentile(image, 5)
    in_max = np.percentile(image, 95)

    out_min = 0.0
    out_max = 255.0

    out = image - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


### Function that calculates NDVI pixel by pixel and returns it as a grayscale [0,255] luminosity value
def calculate_ndvi(image):
    blue, green, red = cv2.split(image)
    bottom = (red.astype(float) + blue.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (blue.astype(float) - red) / bottom
    return ndvi


### Class to serve as the norm of the NDVI plot
class MidpointNormalize(colors.Normalize):

    # Constructor
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0.0, 0.5, 1.0]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))
    

### Function that interprets NDVI and returns a 'matplotlib' plot, and also saves the plot as a '.png' (to save space) image
def interpret_ndvi(ndvi_grayscale, nr):
    # Set min/max NDVI values [-1,1]
    min = numpy.nanmin(ndvi_grayscale)
    max = numpy.nanmax(ndvi_grayscale)

    # Set a specific midpoint. Choose the mean 0; offset towards positive vegetation to best simulate natural conditions
    mid = 127.5

    # Create original NDVI COLORMAP:
    # sample the colormaps that you want to use; use 50+215 = 255 colors (as when we apply the grayscale, the pixel values are [0,255])
    colors1 = plt.cm.gray(np.linspace(0, 0.8, 85))
    colors2 = plt.cm.Spectral(np.linspace(0.12, 0.925, 170))
    # combine them and build a new colormap
    colors = np.vstack((colors1, colors2))
    colormap = mcolors.LinearSegmentedColormap.from_list('colormap', colors)

    # Apply ColorMap
    norm = MidpointNormalize(vmin = min, vmax = max, midpoint = mid)
    fig = plt.figure(figsize=(10,10))

    ax = fig.add_subplot(111)

    # Use 'imshow' to specify: grayscale NDVI image, colormap, and norm (NDVI range is included through the norm) for the legend (colorbar)
    cbar_plot = ax.imshow(ndvi_grayscale, cmap = colormap, norm = norm)

    # Turn off the display of axis labels 
    ax.axis('off')

    # Set a title
    ax.set_title('Terrain - NDVI, no.' + (str(nr) if nr>=100 else ('0'+str(nr) if nr>=10 else '00'+str(nr))), fontsize = 14, fontweight = 'bold')

    # Configure the colorbar
    cbar = fig.colorbar(cbar_plot, orientation='vertical', shrink = 0.6)
    cbar.ax.set_yticklabels(['-1.0','-0.6','-0.2','+0.2','+0.6','+1.0'])

    # Show plot
    # plt.show()
    # Save plot as image
    image_name = (str(nr) if nr>=100 else ('0'+str(nr) if nr>=10 else '00'+str(nr))) + '-terrain_ndvi.png'
    fig.savefig(image_name, dpi=200, bbox_inches='tight', pad_inches=0.05)

    return plt



### Procedural function for the Terrain NDVI procedure
def Terrain_Interpretation_NDVI(original_im, nr):
    # Generate the contrasted image 'constrasted' from the original image 'original_im'
    contrasted = constrast_stretch(original_im)

    # Calculate the NDVI from the contrasted image (better detection and differentiation)
    ndvi = calculate_ndvi(contrasted)
    # The image 'ndvi' is completely black; enhance its contrast to view it in grayscale (white to black)
    ndvi_contrasted = constrast_stretch(ndvi)
   
    # Color map the image 'ndvi_contrasted' to final color mapped version 'color_mapped_image'
    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    #color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    color_mapped_image = interpret_ndvi(color_mapped_prep, nr) # saved as a 'matplotlib' plot

    return color_mapped_image



for idx in range(0,537):
    image_string = "image" + str(idx) + ".jpg"
    image = Image.open(image_string)
    ndvi_map = Terrain_Interpretation_NDVI(image,idx)