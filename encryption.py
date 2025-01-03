import cv2
import numpy as np
import matplotlib.pyplot as plt

class encryption:
    
    def __init__(self):
        self.__coordinateSet: set[str] = set()
        self.frame = None
        self.image = None
        
        # dictionary with values ​​for the key
        self.settingKey: dict = {
            
            # image
            "xImage": 0,
            "yImage": 0,
            
            # frame
            "xFrame": 0,
            "yFrame": 0,
            "add": 0,
            "endChar": 0,
        }
    
    def __getTemplate(self) -> None:
    
        """
        HEIGHT == y == row
        WIDTH == x == column
        """
        
        HEIGHT, WIDTH, RGB = 256, 256, 3
        heightImage, widthImage = 720, 1280 

        self.image = np.random.randint(0, 256, (heightImage, widthImage, RGB), dtype=np.uint8)
        self.frame = np.random.randint(0, 256, (HEIGHT, WIDTH, RGB), dtype=np.uint8)
        
        while True:
        
            try:
                yRandon = np.random.randint(0, heightImage)
                xRandom= np.random.randint(0, widthImage)
                self.image[yRandon + HEIGHT]
                self.image[xRandom + WIDTH]
                
                self.settingKey["yImage"] = str(yRandon)
                self.settingKey["xImage"] = str(xRandom)
                
                break
            except:
                pass
    
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
    
    def __createImage(self, filePath: str) -> None:
        
        # We choose an initial position that is in accordance with the position in which it is located.
        yImage = int(self.settingKey["yImage"])
        xImage = int(self.settingKey["xImage"])
        
        self.image[
            yImage:yImage + self.frame.shape[0],
            xImage:xImage + self.frame.shape[1]
        ] = self.frame
        
        if not cv2.imwrite(filePath, self.image):
            raise ValueError(f"Failed to save the image to {filePath}")
        
        return
    
    def __getImage(self, file: str) -> None:   
        
        try:
            self.image = cv2.imread(file)
        except:
            raise ValueError("Error loading file.")
        
        yImage = int(self.settingKey["yImage"])
        xImage = int(self.settingKey["xImage"])
        
        self.frame = self.image[
            yImage:yImage + 256,
            xImage:xImage + 256
        ]
    
    def encrypt(self, message: str, filePath: str) -> str: 
    
        
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
        self.settingKey["add"] = str(add)
        # ---
        
        # we choose the value that marks the end of the chain
        endChar = np.random.randint(0, 255)
        while endChar in messageSet or (endChar + add) > 255:
            endChar = np.random.randint(0, 255)
        self.settingKey["endChar"] = str(endChar)
        # we add the final value to the list
        messageList.append(endChar)
        # ---
        
        # get a random image and frame
        self.__getTemplate()
        
        # we choose the first values ​​to start
        x, y = self.__getCoordinates()
        self.settingKey["xFrame"] = str(x)
        self.settingKey["yFrame"] = str(y)
        # ---
        
        # We start saving the values ​​in each pixel
        for char in messageList:
            nextX, nextY = self.__getCoordinates()
            newChar = char + add
            self.frame[x, y] = [nextX, nextY, newChar]
            x, y = nextX, nextY
        # ---
        
        # we save the image and create the key
        secretKey = "x".join(self.settingKey.values())
        self.__createImage(filePath)
        # ---
        
        # we reset the class attributes
        self.__coordinateSet = set()
        
        return secretKey
    
    def decrypt(self, file: str, key: str) -> str:
        
        disarmKey = key.split("x")
        self.settingKey: dict = {
            
            # image
            "xImage": int(disarmKey[0]),
            "yImage": int(disarmKey[1]),
            
            # frame
            "xFrame": int(disarmKey[2]),
            "yFrame": int(disarmKey[3]),
            "add": int(disarmKey[4]),
            "endChar": int(disarmKey[5]),
        }
        
        self.__getImage(file)
        
        x, y = self.settingKey["xFrame"], self.settingKey["yFrame"]
        subtraction = self.settingKey["add"]
        endChar = self.settingKey["endChar"]
        
        message: list[str] = []
        count = 0
        while True:
            nextX, nextY, char = self.frame[x, y]
            newChar: int = char - subtraction
            
            if newChar != endChar:
                message.append(chr(newChar))
                x, y = nextX, nextY
            else:
                break
            
            count +=1
            if count>1000:
                print("error")
                break
        return "".join(message)

    def seeImage(self) -> None:
        if self.image is not None:
            plt.imshow(self.image)
            plt.axis('off')
            plt.show()
        else:
            raise ValueError("There is not any image.")
    
    def seeFrame(self) -> None:
        if self.image is not None:
            plt.imshow(self.frame)
            plt.axis('off')
            plt.show()
        else:
            raise ValueError("There is not any frame.")