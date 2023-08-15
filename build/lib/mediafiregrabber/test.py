import requests

# PyPI API endpoint for package uploads
upload_url = 'https://upload.pypi.org/legacy/'

# Replace these with your actual PyPI username and password/token
username = 'swargarajbhowmik'
password = 'pypi-AgEIcHlwaS5vcmcCJDE5Y2UyMjBhLTZmN2QtNDNlOS05MTJlLTVlNzNkZTU4OWEzMwACKlszLCIyNzgxMDhhMS1kNDQ0LTQ0YmItODViNS0xNGUxMGRhOThhYjciXQAABiAq_X34ZaAGyBi_qOcWOQ7uAatnB2G7mkB1_JBZlVNEzQ'

# Path to the distribution package you want to upload
package_file = 'dist/my_package-0.1.tar.gz'

# Open the package file
with open(package_file, 'rb') as f:
    package_data = f.read()

# Set the POST data for the upload
data = {
    ':action': 'file_upload',
    'protocol_version': '1',
}
files = {
    'content': (package_file, package_data)
}

# Make the POST request to upload the package
response = requests.post(upload_url, data=data, files=files, auth=(username, password))

# Check the response
if response.status_code == 200:
    print('Package uploaded successfully!')
else:
    print('Package upload failed.')
    print(response.text)
