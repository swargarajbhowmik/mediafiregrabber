from setuptools import setup, find_packages

setup(
    name="mediafiregrabber",
    version="1.3",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mediafiregrabber = mediafiregrabber.cli:download'
        ],
    },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "tqdm",
        "urllib3",
        "asyncio",
        "aiohttp"
    ],
    author="Swargaraj Bhowmik",
    author_email="contact@swargarajbhowmik.me",
    description="Simple Python Package for MediaFire File Download and Information Retrieval",
    license="MIT",
    url="https://github.com/swargarajbhowmik/mediafiregrabber",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
