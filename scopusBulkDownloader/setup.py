from setuptools import setup

setup(
    name='scopusBulkDownloader',
    version='0.1.0',    
    description='Scrape Abstract and Authors from Scopus',
    url='https://github.com/andrearoota/bachelorThesis',
    author='Andrea Rota',
    author_email='andrea.rota.98@gmail.com',
    license='MIT',
    python_requires='>=3.9',
    packages=['src'],
    scripts=['src/scopusBulkDownloader'],
    install_requires=['pandas==2.1.2',
                      'pymongo==4.5.0',
                      'pyspark==3.4.1',
                      'python-dotenv==1.0.0',
                      'pybliometrics==3.5.2'
                      ]
)
