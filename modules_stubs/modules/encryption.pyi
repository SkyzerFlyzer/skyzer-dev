class Encryption:
    """
    This class is used to encrypt and decrypt text using a key.
    """

    def __init__(self, key: str) -> None:
        """
        Initializes the encryption class with the given key.
        :param key:
        """
        ...

    def encrypt(self, text: str) -> str:
        """
        Encrypts the given text using the key.
        :param text: Unencrypted text
        :return: Encrypted text
        """
        ...
    
    def decrypt(self, text: str) -> str:
        """
        Decrypts the given text using the key.
        :param text: The encrypted text
        :return: The decrypted text
        """
        ...
    
    