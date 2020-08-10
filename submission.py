
from kaggle_environments.envs.halite.helpers import ShipAction, Board, ShipyardAction
import math


directions = [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST]
ship_states = {}


def euclidean_distance(from_pos, to_pos):
    x1, y1 = from_pos
    x, y = to_pos
    distance = math.sqrt(math.pow(x-x1, 2) + math.pow(y-y1, 2))
    return distance


def get_dir_to(from_pos, to_pos):
    distance = 0
    max_idx = 0
    distances = []
    for idx, coord in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
        next_from_pos = from_pos - coord
        calculated_distance = euclidean_distance(next_from_pos, to_pos)
        if calculated_distance >= distance:
            distance = calculated_distance
            max_idx = idx
    return directions[max_idx]


def ship_collect(ship):
    pass


def ship_deposit(ship):
    pass


def spawn(shipyard):
    possible = []
    for direction in [shipyard.cell.north, shipyard.cell.east, 
                      shipyard.cell.south, shipyard.cell.west]:
        if direction.ship is not None:
            possible.append(direction)
    if len(possible) == 0:
        return ShipyardAction.SPAWN


def agent(obs, config):
    size = config.size
    board = Board(obs, config)
    me = board.current_player
    
    if len(me.ships) < 5 and len(me.shipyards) > 0:
        me.shipyards[0].next_action = spawn(me.shipyards[0])
    
    if len(me.shipyards) == 0 and len(me.ships) > 0:
        me.ships[0].next_action = ShipAction.CONVERT
            
    for ship in me.ships:
        if ship.next_action == None:
            if ship.halite < 200:
                ship_states[ship.id] = 'COLLECT'
            if ship.halite > 500:
                ship_states[ship.id] = 'DEPOSIT'
            
            if ship_states[ship.id] == 'COLLECT':
#                 print("Ship is collecting {}".format(ship.position))
                if ship.cell.halite < 100:
                    neighbours = [ship.cell.north, ship.cell.east, 
                                  ship.cell.south, ship.cell.west]
                    possible_moves = []
                    for cell in neighbours:
                        if cell.ship is None:
                            possible_moves.append(cell.halite)
                    
                    best = max(range(len(possible_moves)), key=possible_moves.__getitem__)
                    ship.next_action = directions[best]
            if ship_states[ship.id] == 'DEPOSIT':
#                 print('Ship is returning {}, ship cargo {}, yard location {}'.format(ship.position, ship.halite, me.shipyards[0].position))
                direction = get_dir_to(ship.position, me.shipyards[0].position)
                if direction:
                    ship.next_action = direction
    return me.next_actions
