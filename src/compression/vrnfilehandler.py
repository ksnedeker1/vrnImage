import struct
import os


def vrn_compress(img, vor, averages, filename, directory='./'):
    """
    Store a collection of points and color averages as a .vrn compressed file.
    """
    rows, cols = img.shape[:2]
    # Header: width, height, points count
    data = [struct.pack('<III', cols, rows, len(vor.points))]
    # Coordinates and Colors
    for coord, avg in zip(vor.points, averages):
        # little-endian, 2x unsigned short (max dim.: 65535), 3x unsigned char (1 byte int, RGB in [0, 255])
        data.append(struct.pack('<HHBBB', int(coord[0]), int(coord[1]), int(avg[0]), int(avg[1]), int(avg[2])))
    file_path = f"{directory}/{filename}.vrn"
    with open(file_path, 'wb') as f:
        f.write(b''.join(data))
    return os.path.getsize(file_path)


def vrn_decompress(filename, directory='./'):
    """
    Decompress a .vrn file into rows, cols, num_points, coords, averages.
    """
    with open(f"{directory}/{filename}.vrn", 'rb') as f:
        # Read header
        cols, rows, num_points = struct.unpack('<III', f.read(12))
        # unpack coords and average colors
        coords = []
        averages = []
        for _ in range(num_points):
            col, row, r, g, b = struct.unpack('<HHBBB', f.read(7))
            coords.append((col, row))
            averages.append((r, g, b))
        return (rows, cols, num_points), coords, averages
