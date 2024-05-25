# Password Manager

This is a command-line password manager that uses the hash of a specified file as the master key. The manager supports adding, retrieving, deleting, and suggesting passwords for various accounts.

## Features

1. **Master Key from File**: Generates an encryption key based on the hash of a specified file.
2. **Password Management**:
   - **Add Password**: Add a password for a specified service and account.
   - **Get Password**: Retrieve the password for a specified service and account.
   - **Delete Password**: Delete the password for a specified service and account.
   - **Suggest Password**: Generate and suggest a random password.

## Usage

### Command-Line Arguments

- `--key-file` (required): Path to the master key file.
- `--add`: Add a password for a specified service and account.
- `--get`: Retrieve the password for a specified service and account.
- `--delete`: Delete the password for a specified service and account.
- `--suggest`: Suggest a random password.
- `--service`: The service for which the action is performed.
- `--account`: The account for which the action is performed.
- `--password`: The password to add for an account (used with `--add`).
- `--length`: Length of the suggested password (used with `--suggest`).

### Examples

#### Adding a Password

```sh
python password_manager.py --key-file /path/to/master/key/file --add --service "example.com" --account "user@example.com" --password "my_secure_password"
```

#### Retrieving a Password

```sh
python password_manager.py --key-file /path/to/master/key/file --get --service "example.com" --account "
```

#### Deleting a Password

```sh
python password_manager.py --key-file /path/to/master/key/file --delete --service "example.com" --account "
```

#### Suggesting a Password
The length paramater can be ommited to use the default length of 12 characters.

```sh
python password_manager.py --key-file /path/to/master/key/file --suggest --length 16
```

# Installation
1. Clone the repository.
2. Install the required packages using pip:
```sh
pip install -r requirements.txt
```

# Requirements
* Python 3.6+
* cryptography
* colored

# Licence
This project is licensed under the MIT License.
