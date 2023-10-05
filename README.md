# vrnImage

A demonstrative application for a novel image compression algorithm using Voronoi diagrams using a blend of
mathematics, graphics, image processing, and parallelization techniques. By leveraging the geometric properties
of Voronoi diagrams, the compression process is able to approximate an image's visual contents with a fully 
variable compression ratio determined by the user. This application demonstrates the process with real-time 
visual representations of each process state as they complete. Once the compression process has completed, the 
user can step through brief explanations of each intermediary state of the process alongside visualizations of 
these states with the image data they just compressed.


### What are Voronoi Diagrams?

A Voronoi diagram is a plane partitioning scheme whereby subsets of points are grouped into regions 
based on their proximity to that region's seed point. The vital distinction is that all points in a given 
Voronoi cell share the common trait of being closest to the seed of that cell. In the context of this novel 
compression algorithm, these seed points can be considered as 'representative points', and their corresponding 
Voronoi cells approximate the areas of the image they influence. By selectively sampling a set of representative 
points, bias may be introduced into the compression process such that data loss occurs to a lesser degree 
in areas with greater edge strength and texturing.


### How It Works

1. **Conversion to CIELAB**: The input image is converted to CIELAB. The CIELAB color space is composed of 
one luminance channel and two chromatic axes blue-yellow and green-red. This color space better matches human 
visual perception, and improves the effectiveness of the next step.
2. **Edge Detection**: Sobel edge detection is conducted on each channel of the CIELAB color space to classify
pixels based on edge and texture salience. The results of edge detection on each channel are merged pixel-wise using 
a maximum operation to preserve the most salient observation of each pixel in any of the three channels.
3. **Weighted Sampling**: The combined results of the edge detection process are normalized and used as a heatmap.
Weighted random sampling uses this heatmap to select a set of representative points to be used in constructing the 
Voronoi diagram.
4. **Voronoi Diagram Construction and Color Averaging**: Using the set of representative points as seeds, a Voronoi 
diagram is constructed. The color value of pixels in each cell of the Voronoi diagram are averaged.
5. **Storage and Reconstruction**: The compressed representation of the image is composed of pairs, with each pair
consisting of a representative point's coordinate and the average color value associated with that the cell of that 
representative point. During reconstruction, these representative points are used again as seeds in the same 
deterministic Voronoi diagram algorithm, with the linked color values used to fill the output pixels
contained in each cell.
6. **Metrics Evaluation and Reconstruction**: For the demonstrative purposes of this project, various metrics 
are calculated and displayed to the user, and the compressed image is reconstructed in the GUI.



### Features

- **Interactive GUI**: Built with PyQt5, the GUI is composed of collapsible tabs, an automatically-updated status bar 
and infographic area, and a customized QGraphicsView display area to accommodate zooming and scrolling.
- **Real-time Updates**: As each step of the compression process completes, a generated visual representation is shown 
to the user. This includes the heatmap, the set of representative points, the Voronoi diagram with color bins 
corresponding to cell size, and the reconstruction of the compressed image.
- **Metrics Microservice**: Written by a colleague, a microservice handles the calculation of some metrics such as 
MSE and PSNR.
- **Configurable Compression**: The user can define custom parameter values for Samples: the number of 
representative points, Sampling Linearity: exponential scaling of strength values in the resulting heatmap, Seed: 
the value used to initialize the PRNG, and can toggle the display of demonstrative elements including the visualization 
of compression states and their corresponding explanations.
- **Process Control**: The user can choose from a selection of supplied example images or upload their own. Once the 
process is started, the user can choose to halt it at any time.


### Plans for Expansion

- **GUI Expansion**: Implement additional features such as the ability to save and load configurations, refine the 
halt process, and introduce more metrics.
- **Metrics Microservice**: Opt for a simpler microservice format than the current one provided by a colleague. 
Consider the utility of offloading metrics calculations to a microservice given their relatively low computational 
complexity.
- **Optimize!**: The image reconstruction process is partially vectorized, but unrefined and slow. The compression 
process is on a separate thread from the GUI, but should be parallelized to improve speed - consider a worker pool 
similar to the one made for the mandelbrot_diver project.
- **Auxiliary Tools**: Consider adding additional tools such as a batch processing tool or a CLI-based tool.