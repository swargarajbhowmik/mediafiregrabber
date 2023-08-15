# <img src="https://seeklogo.com/images/M/mediafire-logo-8057F17F6B-seeklogo.com.png" alt="Mediafire logo" width="50"> MediaFireGrabber (Python Edition)
A simple Python package that provides an easy-to-use interface for downloading files from MediaFire and retrieving information about them.

## Features

- Download files from MediaFire by providing the file URL.
- Retrieve information about files, such as name, size, creation date, and more.

## Installation

You can install MediaFireGrabber using pip:

```bash
pip install mediafiregrabber
```

## Usage

### Retrieving File Information

```python
import mediafiregrabber

# For Brief Information
print(mediafire.info(url))

# For Finding File Name
print(mediafiregrabber.name(url))

# For Finding File Size
print(mediafiregrabber.size(url))

# For Finding Uploading Date
print(mediafiregrabber.uploaddate(url))

# For Finding Format of the file to be downloaded (PDF, ZIP, RAR...)
print(mediafiregrabber.format(url))

# For Finding Uploader's Country
print(mediafiregrabber.uploadregion(url))

# For Finding Direct Download Link
print(mediafiregrabber.downloadlink(url))
```

### Download Files
```python
import mediafiregrabber

mediafire.download(url)
```

### CLI Usage
```bash
$ mediafiregrabber <url1> <url2>...
```

Make sure to replace url with actual URLs as needed.

## License
This project is licensed under the MIT License

## Contribution
Contributions are welcome! If you have any feature suggestions, bug reports, or pull requests, please open an issue or a pull request on GitHub.

## Disclaimer
This package is developed independently and is not affiliated with or endorsed by MediaFire.

[![PyPI version](https://badge.fury.io/py/mediafiregrabber.svg)](https://pypi.org/project/mediafiregrabber/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
