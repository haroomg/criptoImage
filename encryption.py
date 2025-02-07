import cv2
import numpy as np

class encryption:
    
    def __init__(self):
        self.__coordinateSet: set[str] = set()
        self.frame: np.array = None
        self.image: np.array = None
        self.xImage: int = None
        self.yImage: int = None
        self.xFrame: int = None
        self.yFrame: int = None
        self.add: int = None
        self.end: int = None
    
    def __getTemplate(self) -> None:
    
        """
        HEIGHT == y == row
        WIDTH == x == column
        """
        
        HEIGHT, WIDTH, RGB = 256, 256, 3
        heightImage, widthImage = 800, 800 

        self.image = np.random.randint(0, 256, (heightImage, widthImage, RGB), dtype=np.uint8)
        self.frame = np.random.randint(0, 256, (HEIGHT, WIDTH, RGB), dtype=np.uint8)
        
        while True:
        
            try:
                yRandon = np.random.randint(0, heightImage)
                xRandom= np.random.randint(0, widthImage)
                self.image[yRandon + HEIGHT]
                self.image[xRandom + WIDTH]
                
                self.yImage = yRandon
                self.xImage = xRandom
                
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
        yImage = self.yImage
        xImage = self.xImage
        shape = self.frame.shape
        
        self.image[
            yImage:yImage + shape[0],
            xImage:xImage + shape[1]
        ] = self.frame
        
        if not cv2.imwrite(filePath, self.image):
            raise ValueError(f"Failed to save the image to {filePath}")
    
    def __getImage(self, file: str) -> None:   
        
        try:
            self.image = cv2.imread(file)
        except:
            raise ValueError("Error loading file.")
        
        y = self.yImage
        x = self.xImage
        val = 256
        self.frame = self.image[y:y + val, x:x + val]
    
    def __setSettingKey(self, key: str) -> None:
        disarmKey = key.split("x")
        self.xImage = int(disarmKey[0])
        self.yImage = int(disarmKey[1])
        self.xFrame = int(disarmKey[2])
        self.yFrame = int(disarmKey[3])
        self.add = int(disarmKey[4])
        self.end = int(disarmKey[5])
    
    def __resetSettingKey(self) -> None:
        
        self.xImage = None
        self.yImage = None
        self.xFrame = None
        self.yFrame = None
        self.add = None
        self.end = None
    
    def __getSecretKey(self) -> str:
        
        return "x".join(
            [
                str(self.xImage),
                str(self.yImage),
                str(self.xFrame),
                str(self.yFrame),
                str(self.add),
                str(self.end)
            ]
        )
    
    def encrypt(self, message: str, filePath: str) -> str: 
        
        # we validate that the characters are valid
        messageList: list[int] = [ord(char) for char in message]
        if any(val > 255 for val in messageList):
            raise ValueError("The message contains invalid characters (only ASCII characters are allowed).")
        # ---
        
        # we choose a sum value to change the current value
        messageSet: set[int] = set(messageList)
        self.add = np.random.randint(0, 100)
        while any((char + self.add) > 255 for char in messageSet):
            self.add = np.random.randint(0, 100)
        # ---
        
        # we choose the value that marks the end of the chain
        self.end = np.random.randint(0, 255)
        while self.end in messageSet or (self.end + self.add) > 255:
            self.end = np.random.randint(0, 255)
        
        # we add the final value to the list
        messageList.append(self.end)
        # ---
        
        # get a random image and frame
        self.__getTemplate()
        
        # we choose the first values ​​to start
        x, y = self.__getCoordinates()
        self.xFrame = x
        self.yFrame = y
        # ---
        
        # We start saving the values ​​in each pixel
        for char in messageList:
            nextX, nextY = self.__getCoordinates()
            newChar = char + self.add
            self.frame[x, y] = [nextX, nextY, newChar]
            x, y = nextX, nextY
        # ---
        
        # we save the image
        self.__createImage(filePath)
        
        # we reset the class attributes
        self.__coordinateSet = set()
        
        key = self.__getSecretKey()
        self.__resetSettingKey()
        
        return key
    
    def decrypt(self, file: str, key: str) -> str:
        
        self.__setSettingKey(key)
        self.__getImage(file)
        
        x, y = self.xFrame, self.yFrame
        subtraction = self.add
        end = self.end
        
        message: list[str] = []
        
        while True:
            nextX, nextY, char = self.frame[x, y]
            newChar: int = char - subtraction
            
            if newChar != end:
                message.append(chr(newChar))
                x, y = nextX, nextY
            else:
                break
        
        self.__resetSettingKey()
        return "".join(message)