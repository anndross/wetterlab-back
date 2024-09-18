def parse_coordinates(coordinates):
    try: 
        return [float(coord) for coord in coordinates]
    except: return [None, None]