import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
td_welcome_img_path = os.path.join(curr_dir, "icon.png")

td_welcome = f"""
    <h1>Welcome to vrnImage! <img src="{td_welcome_img_path}" style="float: right" width="128" height="128"></h1>
    <p>This is a work-in-progress application which will serve to demonstrate an experimental image
    compression technique using Voronoi diagrams. This area will show explanatory material regarding
    the compression process, as well as tips, hints, and how-tos.</p>
    <p>Once you've selected an image by uploading or choosing an included image file and clicking 
    <i>'Start'</i>, you can use the buttons to the left and right of this area with '&lt;' and '&gt;' symbols 
    to step through the process explanation. This will use examples taken directly from the image you 
    compressed.</p>
    <p>If you do not wish to generate and see explanatory elements, uncheck the <i>'Generate Demonstrative 
    Elements'</i> checkbox under <i>'Advanced Settings'</i>.</p>
    """

td_process_running = """
    <h1>Compressing...</h1>
    <p>Your image is now being compressed. The duration of this process is largely dependent on the size of your 
    input image and the number of sampled coordinates (default: 100000). If the process is taking too long, click
    the <i>'Stop'</i> button.</p>
    <p>While the process runs, you'll see status updates at the bottom of the GUI declaring what part of the 
    process is currently running. Each time a stage of the process finishes, the visual representation of 
    the results of this stage will be shown in the graphics window. Once the process completes, you'll
    be able to go back and view these by using the drop-down menu at the top right, or by clicking through
    the explanations of each step using the '&lt;' and '&gt;' buttons to the left and right of this box.</p>
    """

td_original_image = """
    <h1>The Original Image</h1>
    <p>This is your raw input image. Click the '&lt;' and '&gt;' buttons to the left and right of this box
    to see images representing other stages of the process, or use the drop-down menu at the top right.</p>
    <p>When visually comparing steps of the process and the compressed results of this, note some of the following.</p>
    <ul>
        <li><h3>Color Accuracy:</h3> How accurate are the colors compared to the input image? The process takes
        color averages over each of the Voronoi cells, thus some color sharpness is lost as local maxima and minima 
        are merged, but color accuracy should be high.</li>
        <li><h3>Detail Preservation:</h3> Are fine details lost to the compression? Zoom into areas of high
        detail and compare them to the compressed version. As this is a lossy form of compression, fine details
        will naturally be lost in favor of a smaller file size. If details are too obscured, increase the 
        sample count.</li>
        <li><h3>Edges:</h3> Are edges blurred or less sharp? Zooming in on edges may reveal areas where 
        artifacts extend up or down from edges, with an average color that is somewhere between that of the 
        edge and the neighboring face. This results in a loss of sharpness and edge clarity, but can be
        combated by increasing the linearity constant.</li>
        <li><h3>Gradients:</h3> How are gradients of different lengths affected? Especially dependent on the value 
        of the linearity constant, gradients of different lengths can be represented with varying degrees of 
        accuracy within a single image. Choosing a high linearity constant (increasing preference for edges) will
        more accurately represent short gradients and edges, while choosing a low linearity constant (dissolving
        the importance of edges) will result in more accurate representation of long, smooth gradients, with 
        a loss of detail preservation.</li>
        <li><h3>Noise:</h3> Is graininess or noise removed? Again due to the averaging and loss of local maxima
        and minima, noise is naturally filtered out by the compression process without a substantial change
        to color accuracy.</li>
    </ul>
    """

td_heatmap = """
    <h1>The Heatmap</h1>
    <p>Sobel edge detection is conducted on the input image to construct a heatmap of the same dimensions as
    the input image. Instead of carrying color data, pixels in the heatmap correspond to how substantially
    different that pixel is from its neighbors - how 'strong' of an edge is at this pixel</p>
    <p>The process uses 3x3 horizontal and vertical kernels to detect edge strength. The two are combined
    so that pixels occupying edges of equal strength are given equal weights regardless of edge direction.</p>
    <p>The image is converted from RGB to CIELAB before edge detection is conducted on all channels. CIELAB 
    has channels L* for luminance, A* for red-green offset, and B* for yellow-blue offset. By using CIELAB 
    over RGB, the process can better detect edges on color borders and brightness borders.</p>
    <p>In the image to the right, brighter pixels have a higher likeliness of being sampled while darker pixels 
    have a lower likeliness.</p>
    """

td_sampled_points = """
    <h1>The Sampled Points</h1>
    <p>After the edge detection process is complete and the heatmap is generated, a number of coordinates equal to 
    the 'Samples' parameter are randomly sampled without replacement using the heatmap as a frequency table.</p>
    <p>The more samples present in a locale, the more accurately that locale will be represented in the compressed 
    version of the image. Each sampled coordinate represents the 'center' of a cell, for which all pixels whose 
    closest neighboring sample is that coordinate will have their color averaged with all other neighbors 
    sharing this quality.</p>
    """

td_voronoi_diagram = """
    <h1>The Voronoi Diagram</h1>
    <p>A Voronoi diagram is composed of cells where all points within a cell are closest to a single "seed" or 
    "center" point of that cell compared to any other seed point in the diagram, where all the sampled points from
    the previous step serve as Voronoi "seed" points.</p>
    <p>Larger cells contain more pixels from the original image, and thus will average the color over a larger 
    area. By constructing a heatmap and sampling from it, the resulting Voronoi diagram has smaller cells in 
    areas of higher detail and larger cells in areas with less detail. As a result, we are selectively compressing
    areas of the image based on how detailed or "important" our edge detection algorithm determined them to be.</p>
    <p>Purely to improve the visualization, cells are divided into four size classes and colored accordingly. 
    Q1: Red-Magenta, Q2: Yellow-Orange, Q3: Blue-Green, Q4: Black-Gray. Differences in color within a quartile, 
    such as this difference between an orange and a red cell, are meaningless, and serve solely to differentiate
    individual cells from others in the same size class.</p>
    """

td_compressed_image = """
    <h1>The Compressed Image</h1>
    <p>This is the reconstructed image from the compressed version of the input. If you zoom in, you'll likely be 
    able to identify some individual Voronoi cells.</p>
    <p>If you compare back and forth with the input image and used reasonable settings, you'll notice that detailed 
    areas of the image appear slightly blurred. Similarly, you might notice areas of the image that are somewhere in 
    between being detailed and being flat are the weakest and potentially contain artifacts (Voronoi cells that 
    are too large for the level of detail present) visible without zooming. Do keep in mind the compression ratio 
    (shown in General Metrics) when evaluating, as an image that has been compressed to a high degree is unlikely
    to be a stellar representation of the input.</p>
    <p>If visual defects are most severe in detailed areas of the image, increase the linearity constant. If visual 
    defects are most severe elsewhere, lower the linearity constant. If there is a high degree of detail-loss or 
    artifact introduction throughout the image, increase the number of samples. Extreme settings are capable of
    producing artistic results, especially with low sample counts - I encourage you to experiment!</p>
    """
