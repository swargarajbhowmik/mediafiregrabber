# <img src="assets/logo.png" alt="Mediafire logo" width="50"> MediaFireGrabber [Now Supporting Both Files & Folders] (Python Edition)
A simple Python package that provides an easy-to-use interface for downloading files and folders from MediaFire and retrieving information about them.

## Features

- Download folders and files from MediaFire by providing the folder/file URL.
- Retrieve information about files & folders, such as file name, owner name, size, creation date, and more.

## Installation

You can install MediaFireGrabber using pip:

```bash
pip install mediafiregrabber
```

## Usage

### Full Information Retrieving

```python
import mediafiregrabber

# For Brief Information
print(mediafiregrabber.info(url)) # For Both Files & Folders. 
```

You can also use LoadFilesAndFolders=True as argument to load the files and folders present inside a folder. Default is False.

### Partial Information Retrieving

```python
# For Finding File Name
print(mediafiregrabber.name(url))  # Only For Files

# For Finding File Size
print(mediafiregrabber.size(url)) # Only For Files

# For Finding Uploading Date
print(mediafiregrabber.uploaddate(url)) # Only For Files

# For Finding Format of the file to be downloaded (PDF, ZIP, RAR...)
print(mediafiregrabber.format(url)) # Only For Files

# For Finding Uploader's Country
print(mediafiregrabber.uploadregion(url)) # Only For Files

# For Finding Direct Download Link
print(mediafiregrabber.downloadlink(url)) # Only For Files
```

### Download Files or Folders
```python
import mediafiregrabber

mediafiregrabber.download(url)
```

You can pass save="path" argument along with url too!

### CLI Usage
```bash
$ mediafiregrabber <fileurl> <folderurl>...
```
Similarly, you can use --path argument to add your download location.

Make sure to replace url with actual URLs as needed.

## License
This project is licensed under the MIT License

## Contribution
Contributions are welcome! If you have any feature suggestions, bug reports, or pull requests, please open an issue or a pull request on GitHub.

## Disclaimer
This package is developed independently and is not affiliated with or endorsed by MediaFire.

[![PyPI version](https://badge.fury.io/py/mediafiregrabber.svg)](https://pypi.org/project/mediafiregrabber/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
