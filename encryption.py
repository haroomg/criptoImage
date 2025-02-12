import os
import cv2
import random
import json as js
import numpy as np

class Encryption:
    
    def __init__(self):
        
        self.x_image: int = None
        self.y_image: int = None
        self.x_frame: int = None
        self.y_frame: int = None
        self.end: list[int] = None
        self.frame: np.array = None
        self.image: np.array = None
        self.encrypt_dict: dict = {}
        self.dimension: list[int] = None
        self.__coordinate_set: set[str] = set()
        
        # constans 
        self.SIZE: int = 3
        self.STRINGS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"#$%&\'*+,-./:;[\\]_{} \n"
        self.ASCCI_VALUES: list[int] = [i for i in range(256)]
        self.STRINGS_IN_ASCCI: list[int] = [ord(char) for char in self.STRINGS]
    
    def __get_template(self) -> None:
    
        """
        HEIGHT == y == row
        WIDTH == x == column
        """
        
        height, width, rgb = 256, 256, 3
        height_image, width_image = self.dimension

        self.image = np.random.randint(0, 256, (height_image, width_image, rgb), dtype=np.uint8)
        self.frame = np.random.randint(0, 256, (height, width, rgb), dtype=np.uint8)
    
    def __get_coordinates(self, ) -> tuple[int]:
    
        # we choose the random values of x and y
        while True:
            y, x = np.random.randint(0, 255, size=2)
            coordinates = f'{y} {x}'
            
            # we validate that the coordinates have not been used
            if coordinates not in self.__coordinate_set:
                self.__coordinate_set.add(coordinates)
                break
        
        return y, x
    
    def __create_image(self, file_path: str) -> None:
        
        # We choose an initial position that is in accordance with the position in which it is located.
        y_image = self.y_image
        x_image = self.x_image
        shape = self.frame.shape
        
        self.image[
            y_image:y_image + shape[0],
            x_image:x_image + shape[1]
        ] = self.frame
        
        if not cv2.imwrite(file_path, self.image):
            raise ValueError(f"Failed to save the image to {file_path}")
    
    def __get_image(self, file: str) -> None:   
        
        self.image = cv2.imread(file)
        
        if self.image is None:
            raise ValueError("Error loading file. The file may not exist or is not a valid image.")
        
        y = self.y_image
        x = self.x_image
        val = 256
        self.frame = self.image[y:y + val, x:x + val]
    
    def __reset_setting_key(self) -> None:
        
        self.x_image: int = None
        self.y_image: int = None
        self.x_frame: int = None
        self.y_frame: int = None
        self.end: list[int] = None
        self.frame: np.array = None
        self.image: np.array = None
        self.encrypt_dict: dict = {}
        self.dimension: list[int] = None
        self.__coordinate_set: set[str] = set()
    
    def __encrypt_message(self, message: str) -> list[int]:
    
        encrypt_dict: dict = {
            key:{
                "values": values, 
                "pos":0
                } 
            for key, values in self.encrypt_dict.items()
        }
        encrypt_message: list[int] = []
        
        for char in message:
            
            char: str = ord(char)
            pos: int = encrypt_dict[char]["pos"]
            values : list[int] = encrypt_dict[char]["values"]
            new_char: int = values[pos]
            encrypt_message.append(new_char)
            
            if pos < len(values) - 1:
                encrypt_dict[char]["pos"] += 1
            else:
                encrypt_dict[char]["pos"] = 0
        
        choise_end: int = random.choice(self.end)
        encrypt_message.append(choise_end)
        return encrypt_message
    
    def __decrypt_message (self, message: list[int]) -> str:
        
        values_used: dict = {i:None for i in range(256) if i not in self.end}
        
        for char in self.encrypt_dict.keys():
            values: list[int] = self.encrypt_dict[char]
            for value in values:
                values_used[value] = char
                
        new_message: list[int] = [chr(values_used[val]) for val in message]
        
        return "".join(new_message)
    
    def __get_dict(self, path_file: str = None) -> None:
    
        if not path_file:
            raise ValueError("Path file is required")
        
        if not os.path.exists(path_file):
            raise ValueError("File does not exist")
        
        with open(path_file, "r") as file:
            encryption_dict = js.load(file)
            file.close()
        
        self.end = [int(val) for val in encryption_dict["end"].split(",")]
        self.dimension = [int(val) for val in encryption_dict["dimension"].split(",")]
        self.y_image, self.x_image = [int(val) for val in encryption_dict["image"].split(",")]
        self.y_frame, self.x_frame = [int(val) for val in encryption_dict["frame"].split(",")]
        
        shuffled_string = encryption_dict["str"]
        encrypt = encryption_dict["encrypt"]
        
        for char, values in zip(shuffled_string, encrypt):
            new_char = ord(char)
            new_values = [int(val) for val in values.split(",")]
            self.encrypt_dict[new_char] = new_values
            
    def create_dict(self, path_file: str = None, dimension: list[int] = [500,500]) -> None:
        
        directory = os.path.dirname(path_file)
        
        if not path_file:
            raise ValueError("Path file is required")
        
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")
        
        if len(dimension) != 2:
            raise ValueError("Dimension must be a list of two integers")
        
        height, width = dimension
        if height < 256 or width < 256:
            raise ValueError("Dimension must be greater than 256")
        
        count_values_used: dict[int, bool] = {i:False for i in range(256)}
        encrypt_dict: list[str] = []
        
        to_list = list(self.STRINGS)
        random.shuffle(to_list)
        shuffled_string = ''.join(to_list)
        
        for _ in shuffled_string:
            
            values: list[int] = []
            
            while len(values) < self.SIZE:
                
                choise: int = random.choice(self.ASCCI_VALUES)
                
                if not count_values_used[choise]:
                    values.append(choise)
                    count_values_used[choise] = True
                    
            encrypt_dict.append(
                ",".join([str(val) for val in values])
            )
        
        while True:
            y_image = random.randint(0, height - 1)
            x_image = random.randint(0, width - 1)
            if (x_image + 256 < height) and (y_image + 256 < width):
                break
        
        y_frame, x_frame = np.random.randint(0, 255, size=2).tolist()
        end_message = [val for val in count_values_used if not count_values_used[val]]
        
        general_dict = {
            "str": shuffled_string,
            "dimension": f"{dimension[0]},{dimension[1]}",
            "image": f"{y_image},{x_image}", 
            "frame": f"{y_frame},{x_frame}",
            "end": ",".join([str(end) for end in end_message]),
            "encrypt": encrypt_dict
        }
        
        json_string = js.dumps(general_dict, indent=1)
        
        with open(path_file, "w") as file:
            file.write(json_string)
            file.close()
        
        print("The encryption dictionary has been created")
        return

    def encrypt(self, message: str, file_path: str, encryption_dict_path: str) -> None:         
        
        # we validate that the characters are valid
        valid_message_list: list[int] = [ord(char) for char in message]
        if any(val > 255 for val in valid_message_list):
            raise ValueError("The message contains invalid characters (only ASCII characters are allowed).")
        # ---
        
        self.__get_dict(encryption_dict_path)
        message_list = self.__encrypt_message(message)
        
        # get a random image and frame
        self.__get_template()
        
        # we choose the first values to start
        y = self.y_frame
        x = self.x_frame
        self.__coordinate_set.add(f"{y} {x}")
        # ---
        
        # We start saving the values in each pixel
        for char in message_list:
            next_y, next_x = self.__get_coordinates()
            self.frame[y, x] = [next_y, next_x, char]
            y, x = next_y, next_x
        # ---
        
        # we save the image
        self.__create_image(file_path)
        
        # we reset the class attributes
        self.__reset_setting_key()
        
        return
    
    def decrypt(self, file: str, encryption_dict_path: str) -> str:
        
        self.__get_dict(encryption_dict_path)
        self.__get_image(file)
        
        y, x = self.y_frame, self.x_frame
        end = self.end
        
        message: list[str] = []
        while True:
            next_y, next_x, char = self.frame[y, x]
            
            if char not in end:
                message.append(char)
                y, x = next_y, next_x
            else:
                break
        
        new_message: str = self.__decrypt_message(message)
        self.__reset_setting_key()
        return new_message 