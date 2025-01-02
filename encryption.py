import cv2
import numpy as np
import matplotlib.pyplot as plt

class encryption:
    
    def __init__(self):
        self.__coordinateSet: set[str] = set()
        self.image = None
    
    def __getTemplate(self) -> None:
        
        # get a random image template
        HEIGHT, WIDTH, RGB = 255, 255, 3
        self.image = np.random.randint(0, 256, (HEIGHT, WIDTH, RGB), dtype=np.uint8)
    
    def __getCoordinates(self) -> tuple[int]:
    
        # we choose the random values ​​of x and y
        while True:
            x, y = np.random.randint(0, 255, size=2)
            coordinates = f'{x} {y}'
            
            # we validate that the coordinates have not been used
            if coordinates not in self.__coordinateSet:
                self.__coordinateSet.add(coordinates)
                break
        
        return x, y
    
    def encrypt(self, message: str, filePath: str): 
    
        # dictionary with values ​​for the key
        settingKey: dict = {
            "x": 0,
            "y": 0,
            "add":0,
            "endChar": 0
        } 
        # ---
        
        # we validate that the characters are valid
        messageList: list[int] = [ord(char) for char in message]
        if any(val > 255 for val in messageList):
            raise ValueError("The message contains invalid characters (only ASCII characters are allowed).")
        # ---
        
        # we choose a sum value to change the current value
        messageSet: set[int] = set(messageList)
        add = np.random.randint(0, 100)
        while any((char + add) > 255 for char in messageSet):
            add = np.random.randint(0, 100)
        settingKey["add"] = str(add)
        # ---
        
        # we choose the value that marks the end of the chain
        endChar = np.random.randint(0, 255)
        while endChar in messageSet or (endChar + add) > 255:
            endChar = np.random.randint(0, 255)
        settingKey["endChar"] = str(endChar)
        # we add the final value to the list
        messageList.append(endChar)
        # ---
        
        # get a random image template
        self.__getTemplate()
        
        # we choose the first values ​​to start
        x, y = self.__getCoordinates()
        settingKey["x"] = str(x)
        settingKey["y"] = str(y)
        # ---
        
        # We start saving the values ​​in each pixel
        for char in messageList:
            nextX, nextY = self.__getCoordinates()
            newChar = char + add
            self.image[x, y] = [nextX, nextY, newChar]
            x, y = nextX, nextY
        # ---
        
        # we save the image and create the key
        secretKey = "x".join(settingKey.values())
        if not cv2.imwrite(filePath, self.image):
            raise ValueError(f"Failed to save the image to {filePath}")
        # ---
        
        # we restart the set
        self.__coordinateSet = set()
        return secretKey
    
    def decrypt(self, file: str, key: str):
    
        try:
            image = cv2.imread(file)
        except:
            raise ValueError("Error loading file.")
        
        disarmKey = key.split("x")
        settingKey: dict = {
            "x": int(disarmKey[0]),
            "y": int(disarmKey[1]),
            "add":int(disarmKey[2]),
            "endChar": int(disarmKey[3])
        }
        
        x, y = settingKey["x"], settingKey["y"]
        subtraction = settingKey["add"]
        endChar = settingKey["endChar"]
        
        message: list[str] = []
        while True:
            nextX, nextY, char = image[x, y]
            newChar: int = char - subtraction
            
            if newChar != endChar:
                message.append(chr(newChar))
                x, y = nextX, nextY
            else:
                break
            
        return "".join(message)

    def seeImage(self):
        if self.image is not None:
            plt.imshow(self.image)
            plt.axis('off')
            plt.show()
        else:
            raise ValueError("There is not any image.")