import json as js
import random
import os

SIZE: int = 4
STRINGS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
STRINGS_IN_ASCCI: list[int] = [ord(char) for char in STRINGS]
ASCCI_VALUES: list[int] = [i for i in range(256)]

def create_dict(path_file: str = None) -> None:
    
    directory = os.path.dirname(path_file)
    
    if not path_file:
        raise ValueError("Path file is required")
    
    if not os.path.exists(directory):
        raise ValueError(f"Directory {directory} does not exist")
    
    count_values_used: dict[int, bool] = {i:False for i in range(256)}
    encript_dict: dict[int, int] = {char: None for char in STRINGS_IN_ASCCI}
    
    for char in encript_dict:
        
        values: list[int] = []
        
        while len(values) < SIZE:
            
            choise: int = random.choice(ASCCI_VALUES)
            
            if not count_values_used[choise]:
                values.append(choise)
                count_values_used[choise] = True
                
        encript_dict[char] = values
    
    end_message = [val for val in count_values_used if not count_values_used[val]]
    
    general_dict = {
        "end": end_message,
        "encript": encript_dict
    }
    
    json_string = js.dumps(general_dict)
    
    with open(path_file, "w") as file:
        file.write(json_string)
        file.close()
    
    print("The encryption dictionary has been created")
    return


def get_dict(path_file: str = None) -> dict:
    
    if not path_file:
        raise ValueError("Path file is required")
    
    if not os.path.exists(path_file):
        raise ValueError("File does not exist")
    
    with open(path_file, "r") as file:
        json_file = js.load(file)
        file.close()
    
    return json_file