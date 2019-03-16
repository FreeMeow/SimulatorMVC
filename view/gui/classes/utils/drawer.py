import math
from random import shuffle

ROBOT_RADIUS = 15
ROBOT_FACE_LENGTH = 20

VERTEX_RADIUS = 10
VERTEX_COLOR = 'blue'
VERTEX_TARGET_COLOR = 'magenta'
VERTEX_WIDTH = 3
VERTEX_STARVATION_TEMPLATE = 'ST: {}/{}'
VERTEX_PROBABILITY_TEMPLATE = 'P: {}'
VERTEX_TS_TEMPLATE = 'TS: {}'

CLUSTER_COLORS = ['snow', 'dark slate gray', 'dim gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue','turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki','yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle','thistle2']
shuffle(CLUSTER_COLORS)

DEFAULT_FONT = ('Helvetica',-10)

def create_robot(canvas,position):
    robot_body = canvas.create_oval(
        position.x -  ROBOT_RADIUS,
        position.y -  ROBOT_RADIUS,
        position.x +  ROBOT_RADIUS,
        position.y +  ROBOT_RADIUS,
        outline = 'black',
    )
    
    robot_face = canvas.create_line(
        position.x,
        position.y,
        position.x + ROBOT_FACE_LENGTH,
        position.y,
    )

    return {
        'body': robot_body,
        'face': robot_face,
    }

def update_robot(canvas,robot,position,angle):
    canvas.coords(
        robot['body'],
        position.x -  ROBOT_RADIUS,
        position.y -  ROBOT_RADIUS,
        position.x +  ROBOT_RADIUS,
        position.y +  ROBOT_RADIUS,
    )
    canvas.coords(
        robot['face'],
        position.x,
        position.y,
        position.x + math.cos(angle) * ROBOT_FACE_LENGTH,
        position.y + math.sin(angle) * ROBOT_FACE_LENGTH,
    )

def create_vertex(canvas,vertex):
    v = vertex
    vertex_body = canvas.create_oval(
        v['position'].x - VERTEX_RADIUS,
        v['position'].y - VERTEX_RADIUS,
        v['position'].x + VERTEX_RADIUS,
        v['position'].y + VERTEX_RADIUS,
        outline = 'black',
        width = VERTEX_WIDTH,
        fill = CLUSTER_COLORS[-len(CLUSTER_COLORS) + vertex['cluster']] if 'cluster' in vertex else VERTEX_COLOR
    )

    vertex_starvation_text = canvas.create_text(
        v['position'].x,
        v['position'].y - 40,
        text = VERTEX_STARVATION_TEMPLATE.format(0,v['starvation'],0,0),
        font = DEFAULT_FONT
    )

    vertex_probability_text = canvas.create_text(
        v['position'].x,
        v['position'].y - 30,
        text = VERTEX_PROBABILITY_TEMPLATE.format(v['probability']),
        font = DEFAULT_FONT
    )

    vertex_total_starvation_text = canvas.create_text(
        v['position'].x,
        v['position'].y - 20,
        text = VERTEX_TS_TEMPLATE.format(0),
        font = DEFAULT_FONT
    )

    return {
        'body': vertex_body,
        'text': {
            'starvation': vertex_starvation_text,
            'probability': vertex_probability_text,
            'total_starvation': vertex_total_starvation_text,
        },
    }

def update_vertex(canvas,vertex,vertex_static,vertex_live,frame_index,show_text):
    canvas.itemconfigure(
        vertex['body'],
        outline = VERTEX_TARGET_COLOR if vertex_live['is_target'] else 'black'
    )
    canvas.itemconfigure(
        vertex['text']['starvation'],
        text = VERTEX_STARVATION_TEMPLATE.format(frame_index - vertex_live['last_visit'], vertex_static['starvation']),
        fill = 'red' if frame_index > vertex_live['last_visit'] + vertex_static['starvation'] else 'black',
        state = 'normal' if show_text else 'hidden',
    )
    canvas.itemconfigure(
        vertex['text']['probability'],
        state = 'normal' if show_text else 'hidden',
    )
    canvas.itemconfigure(
        vertex['text']['total_starvation'],
        text = VERTEX_TS_TEMPLATE.format(vertex_live['total_starvation']),
        state = 'normal' if show_text else 'hidden',
    )