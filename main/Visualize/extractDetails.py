def extractDetailsFromFile(filename):
    """
    This function parses the input file to provide an array of relevant information in the required formats

    Args:
        filename: name of the input file

    Returns:
        An array of relevant information

    `Expected format of input file:`
        line 1: Name of .scn whole slide image file
        line 2: Name of .xml annotation file
        line 3: 4 space separated float values representing top-left x-y pair and bottom right x-y pair of the rectangular region we want to tile
        line 4: tilesize

    """
    with open(filename, "r") as file:
        img_path = file.readline()[:-1]
        xml_path = file.readline()[:-1]
        rect_coords = list(map(float, file.readline()[:-1].split()))
        gridsize = float(file.readline()[:-1])
        return [img_path, xml_path, rect_coords, gridsize]