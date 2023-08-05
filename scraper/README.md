# ScraperScopus

`ScraperScopus` is a Python script that allows you to scrape abstracts and authors from Scopus based on the specified criteria.

## Usage

```
usage: scraperScopus [-h] --type {aut,abs} [--urimongo URIMONGO] [--subjarea SUBJAREA] [--start START] [--end END]

Scrape Abstract and Authors from Scopus

optional arguments:
  -h, --help           show this help message and exit
  --type {aut,abs}     aut => get authors from already downloaded abstracts, abs => get abstracts
  --urimongo URIMONGO  MongoDB uri (default: mongodb://localhost:27017/)
  --subjarea SUBJAREA  Represents the subject area code associated with the content category desired (default: COMP)
  --start START        Start year for scrape (default: 1850)
  --end END            End year for scrape (default: 2007)
```

## Arguments

- `--type`: Specifies the type of scraping. Use `aut` to get authors from already downloaded abstracts, or `abs` to get abstracts.
- `--urimongo`: MongoDB URI for connecting to the database. If not provided, the default URI is `mongodb://localhost:27017/`.
- `--subjarea`: Represents the subject area code associated with the content category desired. The default value is `COMP`.
- `--start`: The start year for the scrape. The default value is `1850`.
- `--end`: The end year for the scrape. The default value is `2007`.

## Examples

1. To get authors from already downloaded abstracts in the subject area `COMP` from the year `2000` to `2023`:

```
scraperScopus --type aut --subjarea COMP --start 2000 --end 2023
```

2. To get abstracts in the subject area `BIOC` from the year `2010` to `2021`:

```
scraperScopus --type abs --subjarea BIOC --start 2010 --end 2021
```

3. To get abstracts using the default parameters:

```
scraperScopus --type abs
```

## Requirements

- Python 3.x
- Required Python packages (`scopus`, `pymongo`, `pandas`, `pyspark`, etc.)
- MongoDB server

## License

This project is licensed under the [MIT License](LICENSE).