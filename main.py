from PIL import Image
import random
import math

def arrMap(func,arr):
    result = []
    for item in arr:
        result.append(func(item))
    return result

def toFloat(string):
    return float(string)

def createScene():
    randNum = math.ceil(random.random()*73)
    scenePath = R'C:\Users\logan\OneDrive\Pictures\Screenshots\characters\yolo_dataset\scenes\{}.png'.format(randNum)
    scene = Image.open(scenePath)
    basisx = 440+math.floor(random.random()*560)
    basisy = 150+math.floor(random.random()*510)
    cropped = scene.crop((basisx,basisy,basisx+640,basisy+360))
    return cropped


def createCharacter():
    randNum = math.ceil(random.random()*73)
    charpath = R'C:\Users\logan\OneDrive\Pictures\Screenshots\characters\yolo_dataset\final_images\{}.png'.format(randNum)
    filepath = R'C:\Users\logan\OneDrive\Pictures\Screenshots\characters\yolo_dataset\obj_train_data\{}.txt'.format(randNum)
    character = Image.open(charpath)
    file = open(filepath)

    bounding_box_normalized = file.readline().split()
    file.close()
    bounding_box_normalized = arrMap(toFloat,bounding_box_normalized)

    #random body crop for character img
    character_final = character
    if random.random() > 0.5:
        starting_y = (600*bounding_box_normalized[2])+(300*bounding_box_normalized[4])
        new_y_cap = starting_y+100+math.floor(random.random()*(500-starting_y))
        character_final = character.crop((0,0,300,new_y_cap))
        bounding_box_normalized[2] = (bounding_box_normalized[2]*600)/new_y_cap
        bounding_box_normalized[4] = (bounding_box_normalized[4]*600)/new_y_cap

    #random flip and scale for character img
    flipRand = random.random()
    if flipRand > 0.5:
        character_final = character_final.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        bounding_box_normalized[1] = 1-bounding_box_normalized[1]
    scaleRand = 1/(0.8+(random.random()*3.2))
    character_final = character_final.resize((math.floor(character_final.size[0]*scaleRand),math.floor(character_final.size[1]*scaleRand)))
    return (character_final,bounding_box_normalized)


#big the the image being pasted onto, with small being pasted on
#basis is a tupe (x,y) which defines the location of the upper left corner of small
#bbn is the normalized bounding box for the small image
def smartPaste(big,small,bbn,basis):
    final_basis = [basis[0],basis[1]]
    final_small = small
    if basis[0]+final_small.size[0] > big.size[0]:
        overlap = basis[0]+final_small.size[0]-big.size[0]
        bbn[1] = (bbn[1]*final_small.size[0])/(final_small.size[0]-overlap)
        bbn[3] = (bbn[3]*final_small.size[0])/(final_small.size[0]-overlap)
        final_small = final_small.crop((0,0,final_small.size[0]-overlap,final_small.size[1]))
    if basis[1]+final_small.size[1] > big.size[1]:
        overlap = basis[1]+final_small.size[1]-big.size[1]
        bbn[2] = (bbn[2]*final_small.size[1])/(final_small.size[1]-overlap)
        bbn[4] = (bbn[4]*final_small.size[1])/(final_small.size[1]-overlap)
        final_small = final_small.crop((0,0,final_small.size[0],final_small.size[1]-overlap))
    if basis[0] < 0:
        bbn[1] = ((bbn[1]*final_small.size[0])+basis[0])/(final_small.size[0]+basis[0])
        bbn[3] = (bbn[3]*final_small.size[0])/(final_small.size[0]+basis[0])
        final_small = final_small.crop((-basis[0],0,final_small.size[0],final_small.size[1]))
        final_basis[0] = 0
    if basis[1] < 0:
        bbn[2] = ((bbn[2]*final_small.size[1])+basis[1])/(final_small.size[1]+basis[1])
        bbn[4] = (bbn[4]*final_small.size[1])/(final_small.size[1]+basis[1])
        final_small = final_small.crop((0,-basis[1],final_small.size[0],final_small.size[1]))
        final_basis[1] = 0
    big.paste(final_small,(final_basis[0],final_basis[1],final_basis[0]+final_small.size[0],final_basis[1]+final_small.size[1]),final_small)
    bbn[1] = (final_basis[0]+(bbn[1]*final_small.size[0]))/640
    bbn[2] = (final_basis[1]+(bbn[2]*final_small.size[1]))/360
    bbn[3] = (bbn[3]*final_small.size[0])/640
    bbn[4] = (bbn[4]*final_small.size[1])/360
    return (big,bbn)

def pasteHead(big,small,bbn):
    xrange = big.size[0]-(bbn[3]*small.size[0])
    yrange = big.size[1]-(bbn[4]*small.size[1])
    #this is the basis for the upper left corner of the head
    basisx = math.floor(random.random()*xrange)
    basisy = math.floor(random.random()*yrange)
    #this is the basis for the small image
    actual_x = basisx-math.floor((small.size[0]*bbn[1])-(small.size[0]*bbn[3]*(0.5)))
    actual_y = basisy-math.floor((small.size[1]*bbn[2])-(small.size[1]*bbn[4]*(0.5)))
    return smartPaste(big,small,bbn,(actual_x,actual_y))


myCharacter = createCharacter()
myScene = createScene()
#myPaste = smartPaste(myScene,myCharacter[0],myCharacter[1],(100,100))
#myPaste[0].show()
#print(myPaste[1])
myImage = pasteHead(myScene,myCharacter[0],myCharacter[1])
myImage[0].show()
print(myImage[1])

### Character final and bounding_box_normalized are now in their final state, ready to be pasted onto the scene




