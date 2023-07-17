import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
td_welcome_img_path = os.path.join(curr_dir, "icon.png")

td_welcome = f"""
    <h1>Welcome to vrnImage! <img src="{td_welcome_img_path}" style="float: right" width="128" height="128"></h1>
    <p>This is a work-in-progress application which will serve to demonstrate an experimental image
    compression technique using Voronoi diagrams. This area will show explanatory material regarding
    the compression process, as well as tips, hints, and how-tos.</p>
    <p>Once you've compressed an image by uploading or selecting an included image file and clicking 
    <i>'Start'</i>, you can use the buttons to the left and right of this area with '&lt;' and '&gt;' symbols 
    to step through the process explanation. This will use examples taken directly from the image you 
    compressed.</p>
    <p>If you do not wish to generate and see explanatory elements, uncheck the <i>'Generate Demonstrative 
    Elements'</i> checkbox under <i>'Advanced Settings'</i></p>
    """

td_image_loaded = """
    
    """
