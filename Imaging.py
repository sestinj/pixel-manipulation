import math
import random

from PIL import Image


def open_image(path):
    newImage = Image.open(path)
    return newImage

def save_image(image, path):
    image.save(path, 'png')

def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image

def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return None

    pixel = image.getpixel((i, j))
    return pixel

def difference(x1, y1, x2, y2, image):
    pixel1 = get_pixel(image, x1, y1)
    pixel2 = get_pixel(image, x2, y2)

    diff = 0
    for i in range(3):
        diff += pixel2[i] - pixel1[i]

    return abs(diff)

def howManyNeighbors(image, i, j):
    pixel = get_pixel(image, i, j)
    pixelUp = get_pixel(image, i, j+1)
    pixelRight = get_pixel(image, i+1, j)
    pixelDown = get_pixel(image, i, j-1)
    pixelLeft = get_pixel(image, i-1, j)
    pixelDirections = [pixelUp, pixelRight, pixelDown, pixelLeft]

    neighbors = 0

    for pixel2 in pixelDirections:
        if pixel != pixel2:
            neighbors += 1

    return neighbors

def outline(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()
    currentColor = [255, 0, 0]

    sensitivity = 25
    #If the difference between any 2 pixels is greater than the sensitivity, make a black dot.
    for i in range(width-1):
        for j in range(height-1):
            pixel = get_pixel(image, i, j)
            diffx = difference(i, j, i + 1, j, image)
            diffy = difference(i, j, i, j + 1, image)
            if diffx > sensitivity or diffy > sensitivity:
                pixels[i, j] = (0, 0, 0)
                if currentColor[1] >= 255 & currentColor[2] < 255:
                    currentColor[2] += 1
                elif currentColor[2] >= 255:
                    currentColor = [255, 0, 0]
                else:
                    currentColor[1] += 1
            else:
                pixels[i, j] = (currentColor[0], currentColor[1], currentColor[2])

    #Clean up stray black marks
    cleanliness = 4
    for i in range(1, width-1):
        for j in range(1, height-1):
            if howManyNeighbors(image, i, j) < cleanliness:
                pixels[i, j] = (255, 255, 255)

    return new

def convert_probability(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    colors = {}

    for i in range(width):
        for j in range(height):
            currentPixel = get_pixel(image, i, j)
            for k in range(len(directions)):
                otherPixel = get_pixel(image, i + directions[k][0], j + directions[k][1])
                if not currentPixel in colors: colors[currentPixel] = {}
                if otherPixel in colors[currentPixel]:
                    colors[currentPixel][otherPixel] += 1
                else:
                    colors[currentPixel][otherPixel] = 1

##    for i in range(width):
##        for j in range(height):
##            if not (i == 0 and j == 0):




def convert_squares(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    size = 5

    for i in range(width):
        for j in range(height):
            if i%size == 0 and j%size == 0:
                totals = [0, 0, 0]
                for k in range(i, i + size):
                    for l in range(j, j + size):
                        if k < width and k >= 0 and l < height and l >= 0:
                            pixel = get_pixel(image, k, l)
                            totals[0] += pixel[0]
                            totals[1] += pixel[1]
                            totals[2] += pixel[2]
                for k in range(i, i + size):
                    for l in range(j, j + size):
                        if k < width and k >= 0 and l < height and l >= 0:
                            pixels[k, l] = (int(totals[0]/size**2), int(totals[1]/size**2), int(totals[2]/size**2))

    return new

def convert_hexes(image):
    print("HEXES")

def convert_circles(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    number = 600
    radius = 50

    for k in range(number):
        x = random.randint(1, width)
        y = random.randint(1, height)


        totalColor = [0, 0, 0]
        numberOfPixels = 0
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if math.sqrt((x - i)**2+(y - j)**2) <= radius and i >= 0 and i < width and j >= 0 and j < height:
                    numberOfPixels += 1
                    pixel = get_pixel(image, i, j)
                    totalColor[0] += pixel[0]
                    totalColor[1] += pixel[1]
                    totalColor[2] += pixel[2]

        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if math.sqrt((x - i)**2+(y - j)**2) <= radius and i >= 0 and i < width and j >= 0 and j < height:
                    pixels[i, j] = (int(totalColor[0]/numberOfPixels), int(totalColor[1]/numberOfPixels), int(totalColor[2]/numberOfPixels))

    return new



def convert_wavy(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            red = 255
            green = 255
            blue = 255

            heigh = 8
            widt = 4

            offset = int(heigh*math.cos(1/widt*i))
            if j+offset >= 0 and j + offset < height:
                red = get_pixel(image, i, j+offset)[0]

            offset = int(heigh*math.sin(1/widt*i))
            if j+offset >= 0 and j + offset < height:
                green = get_pixel(image, i, j+offset)[1]

            offset = 0
            if j+offset >= 0 and j + offset < height:
                blue = get_pixel(image, i, j+offset)[2]
            pixels[i, j] = (red, green, blue)

    return new


def convert_blur(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    size = 10

    for i in range(size, width-size):
        for j in range(size, height-size):
            red = 0
            green = 0
            blue = 0


            for k in range(1, size):
                red += get_pixel(image, i, j+k)[0]
                red += get_pixel(image, i, j-k)[0]
                red += get_pixel(image, i+k, j)[0]
                red += get_pixel(image, i-k, j)[0]

                green += get_pixel(image, i, j+k)[1]
                green += get_pixel(image, i, j-k)[1]
                green += get_pixel(image, i+k, j)[1]
                green += get_pixel(image, i-k, j)[1]

                blue += get_pixel(image, i, j+k)[2]
                blue += get_pixel(image, i, j-k)[2]
                blue += get_pixel(image, i+k, j)[2]
                blue += get_pixel(image, i-k, j)[2]
            pixels[i, j] = (int(red/(4*(size-1))), int(green/(4*(size-1))), int(blue/(4*(size-1))))
    return new

def convert_polar(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            total = pixel[0]+pixel[1]+pixel[2]
            if total >= 384:
                pixels[i, j] = (255, 255, 255)
            else: pixels[i, j] = (0, 0, 0)
    return new

def average_background(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    redTotal = 0
    greenTotal = 0
    blueTotal = 0

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            redTotal += pixel[0]
            greenTotal += pixel[1]
            blueTotal += pixel[2]

    num = width*height
    average = (int(redTotal/num), int(greenTotal/num), int(blueTotal/num))
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            if (pixel[0]+pixel[1]+pixel[2])/3 >= 240:
                pixels[i, j] = average
            else:
                pixels[i, j] = pixel

    return new


def convert_opposite(image):
       width, height = image.size

       new = create_image(width, height)
       pixels = new.load()

       for i in range(width):
           for j in range(height):
            pixel = get_pixel(image, i, j)
            if (i+j)%4 == 0:
                pixels[i, j] = (255-pixel[0], 255-pixel[1], 255-pixel[2])
            else: pixels[i, j] = (pixel[0], pixel[1], pixel[2])

       return new

def convert_grayscale(image):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):

            pixel = get_pixel(image, i, j)

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            degree = 5

            total = pow(red, degree) + pow(green, degree) + pow(blue, degree)

            gray = int(pow(total, 1/degree))

            pixels[i, j] = (gray, gray, gray)

    return new

def convert_oneColor(image, colorNumber, alpha):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    if colorNumber > 2:
        colorNumber = 2
    elif colorNumber < 0:
        colorNumber = 0

    for i in range(width):
        for j in range(height):

            color = [0, 0, 0]
            color[colorNumber] = int(get_pixel(image, i, j)[colorNumber]*alpha)

            pixels[i, j] = (color[0], color[1], color[2])

    return new

def convert_random(image, startColor):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    colorDown = {}
    colorRight = {}

    #Add every color in picture to dictionaries
    for i in range(width):
        for j in range(height):
            pixelColor = get_pixel(image, i, j)

            #Strip alpha value
            pixelColor = (pixelColor[0], pixelColor[1], pixelColor[2])

            colorDown[pixelColor] = {}
            colorRight[pixelColor] = {}
    print(1)
    #Fill dictionaries' arrays
    for i in range(1, width):
        for j in range(1, height):
            pixelColor = get_pixel(image, i, j)
            pixelLeft = get_pixel(image, i-1, j)
            pixelUp = get_pixel(image, i, j-1)

            #Strip alpha values
            pixelColor = (pixelColor[0], pixelColor[1], pixelColor[2])
            pixelLeft = (pixelLeft[0], pixelLeft[1], pixelLeft[2])
            pixelUp = (pixelUp[0], pixelUp[1], pixelUp[2])

            if pixelColor in colorDown[pixelUp]:
                colorDown[pixelUp][pixelColor] += 1
            else:
                colorDown[pixelUp][pixelColor] = 1

            if pixelColor in colorRight[pixelLeft]:
                colorRight[pixelLeft][pixelColor] += 1
            else:
                colorRight[pixelLeft][pixelColor] = 1

    for key, value in colorDown.items():
        if value == 0:
            del colorDown[key]

    for key, value in colorRight.items():
        if value == 0:
            del colorRight[key]

    print(2)
    #Create picture
    print(colorDown)
    pixels[0, 0] = startColor
    for i in range(1, width):
        for j in range(1, height):
            #Make a list of probable colors
            colors = {}
            pixelLeft = get_pixel(new, i-1, j)
            pixelUp = get_pixel(new, i, j-1)



            colors = colorDown[pixelUp]
            for key, value in colorRight[pixelLeft].items():
                if key in colors:
                    colors[key] += value
                else:
                    colors[key] = value

            #Default is the start color
            pixels[i, j] = startColor
            #Choose a random color from the list
            total = 0
            for key, value in colors.items():
                total += value
            choosing = True
            number = 0
            while choosing:
                if colors[list(colors.keys())[number]] >= random.randint(0, total):
                    pixels[i, j] = list(colors.keys())[number]
                    choosing = False

    return new


image = open_image("Penguin.png")
save_image(convert_grayscale(image), "NewPenguin.png")
save_image(convert_wavy(image), "WavyImage.png")
exit()
