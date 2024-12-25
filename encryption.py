import cv2
import numpy as np
import matplotlib.pyplot as plt

def encryptMessage(message: str, filePath: str): 
    
    settingKey: dict = {
        "x": 0,
        "y": 0,
        "add":0,
        "endchar": 0
    } 
    
    messageList: list[int] = []
    for char in message:
        val: int = ord(char)
        if val <= 255:
            messageList.append(val)
        else:
            raise ValueError(
                """The message you want to encrypt is not an act, 
                it can only be made up of the ASCII code characters"""
                )
    
    messageSet = set(messageList)
    while True:
        randomValue: int = 100
        add: int = np.random.randint(0, randomValue)
        validAdd: list[int] = [1 for char in messageSet if (char + add) >= 255]
        if not len(validAdd):
            settingKey["add"] = str(add)
            break
    
    while True:
        endchar: int = np.random.randint(0,255)
        if endchar not in messageSet and (endchar + add):
            settingKey["endchar"] = str(endchar)
            break
    
    # get a random image template
    HEIGHT: int = 255
    WIDTH: int = 255
    RGB: int = 3
    image = np.ones((HEIGHT, WIDTH, RGB), dtype=np.uint8)
    
    for x in range(HEIGHT):
        for y in range(WIDTH):
            
            image[x, y] = [
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255),
            ]
            
    coordinateSet = set()
    x = np.random.randint(0, 255)
    y = np.random.randint(0, 255)
    coordinateSet.add(f'{x} {y}')
    settingKey["x"] = str(x)
    settingKey["y"] = str(y)
    
    for char in messageList:
        
        while True:
            nextX = np.random.randint(0, 255)
            nextY = np.random.randint(0, 255)
            coordina = f'{nextX} {nextY}'
            
            if coordina not in coordinateSet:
                coordinateSet.add(coordina)
                break
        
        
        newChar = char + add
        image[x, y] = [nextX, nextY, newChar]
        
        x = nextX
        y = nextY
    
    image[x, y] = [nextX, nextY, endchar]
    
    secretKey = "x".join(settingKey.values())
    
    cv2.imwrite(filePath, image)
    
    return image, secretKey

def decryptMessage(file, key):
    
    try:
        image = cv2.imread(file)
    except:
        raise ValueError("Error loading file.")
    
    disarmKey = key.split("x")
    settingKey: dict = {
        "x": int(disarmKey[0]),
        "y": int(disarmKey[1]),
        "add":int(disarmKey[2]),
        "endchar": int(disarmKey[3])
    }
    
    x = settingKey["x"]
    y = settingKey["y"]
    subtraction = settingKey["add"]
    endchar = settingKey["endchar"]
    
    message: list[str] = []
    while True:
        nextX, nextY, char = image[x, y]
        if char != endchar:
            
            convert = chr(char - subtraction)
            message.append(convert)
            x = nextX
            y = nextY
            
        else:
            break
        
    return "".join(message)

def seeImage(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()