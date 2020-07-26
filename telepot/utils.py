from hashlib import sha512, sha256
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from base64 import b64decode
import os, json
from telepot.exception import DecryptionError

default_path = os.path.abspath('')+'/'


def decrypt_passport_data(_hash, secret, data, private_key, password=None, path=default_path, filepath=default_path):
    """
    Decrypting passport data according to https://core.telegram.org/passport#decrypting-data

    :param _hash:
        hash string that we get from EncryptedCredentials
    :param secret:
        secret string that we get from EncryptedCredentials
    :param data:
        string data that we get from various passport fields
    :param private_key:
        private key pem filename
    :param password:
        ```default : None```
        passphrase for the pem file in case it has one
    :param path:
        ```default : Current path of the working directory```
        location of the private key
    :param filepath:
        ```default : Current path of the working directory```
        location of the passport files
    :return:
        a string that contains the decrypted data.
    """

    """Step 1: Decrypt the credentials secret (secret field in EncryptedCredentials) using your private key"""
    _hash = b64decode(_hash)
    rsa_key = RSA.importKey(open(path+private_key, "rb").read(), passphrase=password)
    cipher = PKCS1_OAEP.new(rsa_key)
    raw_cipher_data = b64decode(secret)
    try:
        secret = cipher.decrypt(raw_cipher_data)
    except:
        """No need to decrypt using private key for EncryptedData and EncryptedFiles"""
        secret = raw_cipher_data
    """Step 2: Use this secret and the credentials hash ( hash field in EncryptedCredentials) to calculate 
    credentials_key and credentials_iv as shown below"""
    data_secret_hash = sha512(secret + _hash).digest()
    data_key = data_secret_hash[:32]
    data_iv = data_secret_hash[32: 48]

    """Step 3:Decrypt the credentials data ( data field in EncryptedCredentials) by AES256-CBC using these
     credentials_key and credentials_iv above."""
    cipher = AES.new(mode=AES.MODE_CBC, key=data_key, iv=data_iv)
    decrypted = cipher.decrypt(b64decode(data) if type(data) != bytes else data)
    data_hash = sha256(decrypted).digest()

    """Step 4: IMPORTANT: At this step, make sure that the credentials hash is equal to SHA256(credentials_data)"""
    if data_hash != _hash:
        raise DecryptionError("The credentials hash is not equal to credentials data")

    """The first byte contains the length of the padding (including that byte). Remove padding to 
    get the file content."""
    output = decrypted[decrypted[0]:]

    return json.loads(output) if type(data) != bytes else open(filepath, 'wb').write(output)


def file_decryptor(bot, data_hash, data_secret, private_key, password, path, file_id):
    file_details = bot.getFile(file_id)
    file_path = file_details['file_path']
    full_path = path + file_path
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    file = bot.download_file(file_id, dest=None)
    in_data = file
    decrypt_passport_data(data_hash, data_secret, in_data, private_key, password, path, filepath=full_path)
    return full_path


def clean_data(bot, all_data, private_key, password=None, path=default_path):
    """
    Transforms the encrypted data to usable data and files.

    :param bot:
        current initialized bot instance
    :param all_data:
        passport object from telepot glance or from msg
    :param private_key:
        private key pem filename
    :param password:
        ```default : None```
        passphrase for the pem file in case it has one
    :param path:
        ```default : Current path of the working directory```
        location of the private key

    :return:
        a dict that contains the decrypted data and extra fields like `file location`.
    """
    credentials, all_fields_data = all_data['credentials'], all_data['data']
    cred_data, secret, _hash = credentials['data'], credentials['secret'], credentials['hash']

    clean_cred_data = decrypt_passport_data(_hash, secret, cred_data, private_key, password, path)
    secure_data = clean_cred_data['secure_data']
    all_data['credentials']['data'] = clean_cred_data
    new_data = []
    for data in all_fields_data:
        data_type = data['type']
        in_secure_data = secure_data.get(data_type, None)
        if in_secure_data:
            contents = secure_data[data_type]
            keys = ['data', 'files', 'front_side', 'reverse_side', 'selfie', 'translation']
            inside_keys = [contents.get(key, None) for key in keys]

            for in_keys, inside_values in zip(keys, inside_keys):
                if in_keys != 'files':
                    if inside_values:
                        data_hash, data_secret = inside_values.values()
                        if in_keys == 'data':
                            in_data = data[in_keys]
                            full_path = default_path
                            output = decrypt_passport_data(data_hash, data_secret, in_data, private_key, password, path,
                                                           filepath=full_path)
                            data[in_keys] = output
                        else:
                            file_id = data[in_keys]['file_id']
                            store_path = file_decryptor(bot, data_hash, data_secret, private_key, password,
                                                        path, file_id)
                            data[in_keys]['file_path'] = store_path
                else:
                    if inside_values:
                        for file in inside_values:
                            data_hash, data_secret = file.values()

                            for value in data[in_keys]:
                                file_id = value['file_id']
                                store_path = file_decryptor(bot, data_hash, data_secret, private_key, password,
                                                            path, file_id)
                                current_index = data[in_keys].index(value)
                                data[in_keys][current_index]['file_path'] = store_path
        new_data.append(data)
    all_data['data'] = new_data

    return all_data
