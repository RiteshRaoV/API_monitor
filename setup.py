from setuptools import setup, find_packages

setup(
    name="api_monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",       
        "geoip2",         
        "psutil",         
        "django",         
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
)
