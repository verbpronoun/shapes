import math
from random import *
from PIL import Image, ImageDraw

WIDTH = 65
HEIGHT = 65
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MIN_DEGREE = 20
MIN_RATIO = 1.3

# img = Image.new(mode='1', size=(WIDTH, HEIGHT), color=BLACK)
# draw = ImageDraw.Draw(img)
# draw.polygon((10,10,10,30,30,30,30,10), fill=WHITE)

# filename = "square1.jpg"
# img.save(filename)

def distance(x1, y1, x2, y2):
    return math.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))

def rotate(x, y, theta):
    radius = distance(x, y, 0, 0)
    theta += math.atan2(y, x)
    return (radius * math.cos(theta), radius * math.sin(theta))

def verify_in_bounds(vertices):
    for x,y in vertices:
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            return False
    return True

def verify_valid_triangle(vertices):
    lengths = []
    for i in range(3):
        for j in range(i+1, 3):
            length = distance(vertices[i][0], vertices[i][1], vertices[j][0], vertices[j][1])
            if length < 10:
                return False
            lengths.append(length)

    for i in range(3):
        # law of cosines lol
        cosine = ((lengths[i%3] ** 2) + (lengths[(i+1)%3] ** 2) - (lengths[(i+2)%3] ** 2)) / (2 * lengths[i%3] * lengths[(i+1)%3])
        if cosine > math.cos(math.radians(MIN_DEGREE)):
            return False

    return True



def get_square_vertices():
    while True: 
        side = uniform(10, WIDTH)
        theta = uniform(-math.pi/4, math.pi/4)
        shift_x = uniform((side - WIDTH)/2, (WIDTH - side)/2)
        shift_y = uniform((side - HEIGHT)/2, (HEIGHT - side)/2)
          
        vertices = (
            (+ side/2, + side/2), 
            (+ side/2, - side/2), 
            (- side/2, - side/2),
            (- side/2, + side/2)
        )

        rotated_vertices = [rotate(x, y, theta) for x,y in vertices]
        shifted_vertices = [((round(x + shift_x + WIDTH/2.0), round(y + shift_y + HEIGHT/2.0))) for x,y in rotated_vertices]
        
        if verify_in_bounds(shifted_vertices):
            return shifted_vertices
        # print('Failed square')

def get_rectangle_vertices():
    while True: 
        w = uniform(10, WIDTH)
        h = uniform(10, HEIGHT)
        if (w / h) < MIN_RATIO and (w / h) > (1 / MIN_RATIO):
            continue
        theta = uniform(-math.pi/4, math.pi/4)
        shift_x = uniform((w - WIDTH)/2, (WIDTH - w)/2)
        shift_y = uniform((h - HEIGHT)/2, (HEIGHT - h)/2)
          
        vertices = (
            (+ w/2, + h/2), 
            (+ w/2, - h/2), 
            (- w/2, - h/2),
            (- w/2, + h/2)
        )

        rotated_vertices = [rotate(x, y, theta) for x,y in vertices]
        shifted_vertices = [((round(x + shift_x + WIDTH/2.0), round(y + shift_y + HEIGHT/2.0))) for x,y in rotated_vertices]
        
        if verify_in_bounds(shifted_vertices):
            return shifted_vertices
        # print('Failed rectangle')

def get_triangle_vertices():
    while True: 
        vertices = [(randint(0, WIDTH), randint(0,HEIGHT)) for i in range(3)]
        if verify_valid_triangle(vertices):
            return vertices
        # print('Failed triangle')


def make_shape(get_shape_vertices, filename):
    img = Image.new(mode='RGB', size=(WIDTH, HEIGHT), color=BLACK)
    draw = ImageDraw.Draw(img)
    draw.polygon(get_shape_vertices(), fill=WHITE)
    img.save(filename)

for i in range(10):
    filename = 'shapes/square' + str(i) + '.jpg'
    make_shape(get_square_vertices, filename)  

for i in range(10):
    filename = 'shapes/rectangle' + str(i) + '.jpg'
    make_shape(get_rectangle_vertices, filename)  

for i in range(10):
    filename = 'shapes/triangle' + str(i) + '.jpg'
    make_shape(get_triangle_vertices, filename)  






