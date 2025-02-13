# Encryption Class

## Overview

The `Encryption` class provides functionality for encrypting and decrypting messages using images. It embeds encrypted data into image frames by manipulating pixel values based on a generated encryption dictionary.

## Features

- **Encryption**: Convert plaintext messages into encrypted data stored within images.
- **Decryption**: Retrieve original messages from encrypted images.
- **Dynamic Dictionary Creation**: Generate a custom encryption dictionary based on specified dimensions and character sets.

## Dependencies

- `opencv-python`: For image processing.
- `numpy`: For numerical operations.
- `json`: For handling JSON data.

## Class Methods

### `__init__(self)`

Initializes the class attributes, including image dimensions, encryption dictionary, and coordinate sets.

### `create_dict(path_file: str, dimension: list[int])`

Creates an encryption dictionary and saves it to the specified file. The dictionary maps characters to their encrypted values.

### `encrypt(message: str, file_path: str, encryption_dict_path: str)`

Encrypts a given message and saves the resulting image to the specified file path using the provided encryption dictionary.

### `decrypt(file: str, encryption_dict_path: str) -> str`

Decrypts an image file and returns the original message using the specified encryption dictionary.

### Private Methods

- `__get_template()`: Generates a random image template for embedding encrypted data.
- `__get_coordinates()`: Chooses random coordinates for embedding data in the image.
- `__create_image(file_path: str)`: Saves the modified image to the specified file path.
- `__get_dict(path_file: str)`: Loads the encryption dictionary from a file.

## Usage Example

```python
# Example usage of the Encryption class
encryption = Encryption()
encryption.create_dict("encryption_dict.json", [500, 500])
encryption.encrypt("Hello, World!", "encrypted_image.png", "encryption_dict.json")
decrypted_message = encryption.decrypt("encrypted_image.png", "encryption_dict.json")
print(decrypted_message)  # Output: Hello, World!
```

## Error Handling

The class includes error handling for invalid inputs, file operations, and image processing to ensure robustness.

## Conclusion

The `Encryption` class is a powerful tool for embedding and retrieving messages within images, providing a unique approach to data security.
