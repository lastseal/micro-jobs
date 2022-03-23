from setuptools import setup

setup(
    name="micro-jobs",
    version="1.1.1",
    description="Micro servicios basados en el módulo schedules",
    author="Rodrigo Arriaza",
    author_email="hello@lastseal.com",
    url="https://www.lastseal.com",
    packages=['micro'],
    install_requires=[ 
        i.strip() for i in open("requirements.txt").readlines() 
    ]
)
