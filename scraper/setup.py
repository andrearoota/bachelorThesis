from setuptools import setup

setup(
    name='scopusScraper',
    version='0.1.0',    
    description='Scrape Abstract and Authors from Scopus',
    url='https://github.com/andrearoota/bachelorThesis',
    author='Andrea Rota',
    author_email='andrea.rota.98@gmail.com',
    license='MIT',
    packages=['src'],
    scripts=['src/scraperScopus'],
    install_requires=['pandas==2.0.3',
                      'pymongo==4.4.1',
                      'pyspark==3.4.1',
                      'python-dotenv==1.0.0'
                      ]
)
