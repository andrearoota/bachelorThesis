# Bibliometric Factors Analysis for Scientific Paper Authors (bachelor thesis)
A comprehensive software solution designed to gather, analyze, and visualize bibliometric factors of scientific paper authors.

## Overview
This project is a culmination of a bachelor's thesis, aiming to provide a holistic tool for bibliometric data collection, analysis, and visualization. It leverages the Scopus API for data acquisition and offers a client-server architecture for data processing and presentation.

## Features
- **Data Collection**: Utilizes the Scopus API to fetch bibliometric data. The [scopusBulkDownloader](https://github.com/andrearoota/bachelorThesis/blob/main/scopusBulkDownloader/src/scopusBulkDownloader) module facilitates this process.
- **Backend Analysis**: The backend, written in Python, employs Flask for web infrastructure. It offers various analyses, including:
  - [Average Coauthors Variation After Years](https://github.com/andrearoota/bachelorThesis/blob/main/backend/flask/analyses.py)
  - [Coauthors Impact on Citations and H-index](https://github.com/andrearoota/bachelorThesis/blob/main/backend/flask/analyses.py)
  - [H-index Influential Articles Timing Analysis](https://github.com/andrearoota/bachelorThesis/blob/main/backend/flask/analyses.py)
  - And more...
- **Frontend Visualization**: The frontend is crafted using TypeScript and React, providing a user-friendly interface for data visualization. The main entry point for the frontend can be found [here](https://github.com/andrearoota/bachelorThesis/blob/main/frontend/src/main.tsx).

## Technologies Used
- **Backend**: Flask, Pandas
- **Data Collection**: Scopus API, Pybliometrics
- **Frontend**: TypeScript, React
- **Data Processing**: Spark, Pandas
- **Database**: MongoDB
- **Containerization**: Docker

## Setup & Installation
1. Clone the repository.
2. Set up Docker and ensure all dependencies are installed.
3. Follow individual setup instructions for [backend](https://github.com/andrearoota/bachelorThesis/blob/main/backend/flask/server.py) and [frontend](https://github.com/andrearoota/bachelorThesis/blob/main/frontend/src/main.tsx).
4. Run the application using Docker.

## License
This project is licensed under the [MIT License](https://github.com/andrearoota/bachelorThesis/blob/main/LICENSE).