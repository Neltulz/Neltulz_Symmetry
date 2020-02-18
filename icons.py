from . import __path__

import bpy
import pickle

iconList = [
    # Icon Name           Icon Dat File
    ['xIcon',            'xIcon.dat'        ],
    ['xIconLeft',        'xIconLeft.dat'    ],
    ['xIconRight',       'xIconRight.dat'   ],

    ['yIcon',            'yIcon.dat'        ],
    ['yIconLeft',        'yIconLeft.dat'    ],
    ['yIconRight',       'yIconRight.dat'   ],

    ['zIcon',            'zIcon.dat'        ],
    ['zIconLeft',        'zIconLeft.dat'    ],
    ['zIconRight',       'zIconRight.dat'   ],
]

i = {} #declare icon dict (this will contain all of the icons that can be used in ui layouts)

#create each icon and add it to the icon dict
for iconDat in iconList:

    fullPathToIcon = f'{__path__[0]}/icons/{iconDat[1]}'

    # "rb" means read bytes
    with open(fullPathToIcon, "rb") as file:
        geo, colors = pickle.load(file)

    iconInfo = (geo, colors)

    #NOTE: iconInfo[0] = geo, #iconInfo[1] = colors

    icon = bpy.app.icons.new_triangles((10, 0), iconInfo[0], iconInfo[1])

    #add icon to dict
    i[ iconDat[0] ] = icon

