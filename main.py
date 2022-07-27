import argparse
import json


def getTileCords(args):

    # When we have tile input process here, for now we fake.
    tile_size = 768

    #square with four tiles
    tile_cords = dict()

    tile_cord0 = dict()
    tile_cord0['x0'] = tile_size * 0
    tile_cord0['x1'] = tile_size * 1
    tile_cord0['y0'] = tile_size * 0
    tile_cord0['y1'] = tile_size * 1
    tile_cord0['confidence'] = .75
    tile_cord0['color'] = 'red'

    tile_cord1 = dict()
    tile_cord1['x0'] = tile_size * 1
    tile_cord1['x1'] = tile_size * 2
    tile_cord1['y0'] = tile_size * 0
    tile_cord1['y1'] = tile_size * 1
    tile_cord1['confidence'] = .9
    tile_cord1['color'] = 'red'

    tile_cord2 = dict()
    tile_cord2['x0'] = tile_size * 0
    tile_cord2['x1'] = tile_size * 1
    tile_cord2['y0'] = tile_size * 1
    tile_cord2['y1'] = tile_size * 2
    tile_cord2['confidence'] = .25
    tile_cord2['color'] = 'green'

    tile_cord3 = dict()
    tile_cord3['x0'] = tile_size * 1
    tile_cord3['x1'] = tile_size * 2
    tile_cord3['y0'] = tile_size * 1
    tile_cord3['y1'] = tile_size * 2
    tile_cord3['confidence'] = .55
    tile_cord3['color'] = 'yellow'

    tile_cords[0] = tile_cord0
    tile_cords[1] = tile_cord1
    tile_cords[2] = tile_cord2
    tile_cords[3] = tile_cord3

    calculated_tile_size = tile_cords[0]['x1'] - tile_cords[0]['x0']

    max_x = 0
    max_y = 0

    for tile_id, coord in tile_cords.items():
        if coord['x1'] > max_x:
            max_x = coord['x1']
        if coord['y1'] > max_y:
            max_y = coord['y1']

    return calculated_tile_size, max_x, max_y, tile_cords

def getTileCordsFile(args):

    with open(args.cord_input_path) as f:
        data = json.load(f)

    # square with four tiles
    tile_cords = dict()
    count = 0
    for tile in data['tiles']:

        tile_cord0 = dict()
        tile_cord0['x0'] = tile['points']['x_s']
        tile_cord0['x1'] = tile['points']['x_e']
        tile_cord0['y0'] = tile['points']['y_s']
        tile_cord0['y1'] = tile['points']['y_e']
        tile_cord0['confidence'] = tile['confidence']
        if tile['confidence'] >= .75:
            tile_cord0['color'] = 'red'
        elif (tile['confidence'] >= .5) and (tile['confidence'] < .75):
            tile_cord0['color'] = 'yellow'
        elif tile['confidence'] < .5:
            tile_cord0['color'] = 'green'
        else:
            print('wtf')
            print(tile)

        tile_cords[count] = tile_cord0
        count = count + 1

    calculated_tile_size = tile_cords[0]['x1'] - tile_cords[0]['x0']

    max_x = 0
    max_y = 0

    for tile_id, coord in tile_cords.items():
        if coord['x1'] > max_x:
            max_x = coord['x1']
        if coord['y1'] > max_y:
            max_y = coord['y1']

    return calculated_tile_size, max_x, max_y, tile_cords

def getLines(calculated_tile_size, max_x, max_y, tile_cords):


    x_line_keys = []

    x_min = 0

    for y in range(0, max_y + calculated_tile_size, calculated_tile_size):
        for x in range(0, max_x + calculated_tile_size, calculated_tile_size):

            if (x > 0):
                xline = dict()
                xline['x0'] = x_min
                xline['x1'] = x
                xline['y'] = y
                x_line_keys.append(xline)
            x_min = x
        x_min = 0

    cx_lines = []

    for xline in x_line_keys:
        match_coords = []
        for tile_id, coord in tile_cords.items():
            if (xline['x0'] == coord['x0']) and (xline['x1'] == coord['x1']) and (xline['y'] == coord['y0']):
                #print(coord)
                match_coords.append(coord['color'])
                #print(match_coords)
            if (xline['x0'] == coord['x0']) and (xline['x1'] == coord['x1']) and (xline['y'] == coord['y1']):
                #print(coord)
                match_coords.append(coord['color'])
                #print(match_coords)

        #print(coord)
        if(len(match_coords) >0):
            if(len(match_coords) == 1):
                xline['color'] = match_coords[0]
                cx_lines.append(xline)
            else:
                if match_coords[0] not in match_coords[1]:
                    xline['color'] = match_coords[0] + '-' + match_coords[1]
                    cx_lines.append(xline)


    return cx_lines




if __name__ == '__main__':

    # create arg parser
    parser = argparse.ArgumentParser(description='OMERO Polyline Generator')

    # general args
    parser.add_argument('--cord_input_path', type=str, default="cords.json", help='information on tile coords')
    #parser.add_argument('--tile_size', type=int, default=768, help='size of tiles')

    args = parser.parse_args()

    #in code
    calculated_tile_size, max_x, max_y, tile_cords = getTileCords(args)
    print(tile_cords)

    #in file
    calculated_tile_size, max_x, max_y, tile_cords = getTileCordsFile(args)
    print(tile_cords)

    exit(0)
    cx_lines = getLines(calculated_tile_size, max_x, max_y, tile_cords)

    for cx_line in cx_lines:
        print(cx_line)