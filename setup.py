import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="advanced-telegram-bot", # Replace with your own username
    version="0.1.5",
    author="minish144 & usual-one",
    author_email="varlamow.col@yahoo.com",
    description="Python library containing utils for telegram bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdallaboratory/advanced-telegram-bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pymongo', 'python-telegram-bot', 'decorator']
)
