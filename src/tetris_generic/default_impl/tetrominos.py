from tetris_generic.tetromino import TetrominoType, WallKickData
from .colour_cell import ColourCell
from tetris_generic.tetromino import shape_from_string

jlstz_wall_kick_data: WallKickData = WallKickData({
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
})

o_wall_kick_data: WallKickData = WallKickData({
    (0, 1): [(0, 0)],
    (1, 0): [(0, 0)],
    (1, 2): [(0, 0)],
    (2, 1): [(0, 0)],
    (2, 3): [(0, 0)],
    (3, 3): [(0, 0)],
    (3, 0): [(0, 0)],
    (0, 3): [(0, 0)],
})

i_wall_kick_data: WallKickData = WallKickData({
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
})

i_tetromino = TetrominoType(
    size=4,
    data=shape_from_string(
        4,
        '    ',
        '****',
        '    ',
        '    '
    ),
    wall_kick_data=i_wall_kick_data,
    filling_cell=ColourCell((0, 255, 255))
)

j_tetromino = TetrominoType(
    size=3,
    data=shape_from_string(
        3,
        '*  ',
        '***',
        '   '
    ),
    wall_kick_data=jlstz_wall_kick_data,
    filling_cell=ColourCell((0, 0, 255))
)

l_tetromino = TetrominoType(
    size=3,
    data=shape_from_string(
        3,
        '  *',
        '***',
        '   '
    ),
    wall_kick_data=jlstz_wall_kick_data,
    filling_cell=ColourCell((255, 127, 0))
)

o_tetromino = TetrominoType(
    size=2,
    data=shape_from_string(
        2,
        '**',
        '**'
    ),
    wall_kick_data=o_wall_kick_data,
    filling_cell=ColourCell((255, 255, 0))
)

s_tetromino = TetrominoType(
    size=3,
    data=shape_from_string(
        3,
        ' **',
        '** ',
        '   '
    ),
    wall_kick_data=jlstz_wall_kick_data,
    filling_cell=ColourCell((0, 255, 0))
)

z_tetromino = TetrominoType(
    size=3,
    data=shape_from_string(
        3,
        '** ',
        ' **',
        '   '
    ),
    wall_kick_data=jlstz_wall_kick_data,
    filling_cell=ColourCell((255, 0, 0))
)

t_tetromino = TetrominoType(
    size=3,
    data=shape_from_string(
        3,
        ' * ',
        '***',
        '   '
    ),
    wall_kick_data=jlstz_wall_kick_data,
    filling_cell=ColourCell((255, 0, 255))
)

tetromino_types: list[TetrominoType] = [
    i_tetromino,
    j_tetromino,
    l_tetromino,
    o_tetromino,
    s_tetromino,
    z_tetromino,
    t_tetromino
]
