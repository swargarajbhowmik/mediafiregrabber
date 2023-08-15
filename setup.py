from setuptools import setup, find_packages

setup(
    name="MediaFireGrabber",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mediafiregrabber = mediafiregrabber.cli:main'
        ],
    },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "tqdm"
    ],
    author="Swargaraj Bhowmik",
    author_email="contact@swargarajbhowmik.me",
    description="Simple Python Package for MediaFire File Download and Information Retrieval",
    license="MIT",
    url="https://github.com/swargarajbhowmik/mediafiregrabber",
)
