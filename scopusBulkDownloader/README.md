# ScopusBulkDownloader

`ScopusBulkDownloader` is a Python script that allows you to download abstracts and authors from Scopus based on the specified criteria.

## Usage

```
usage: scopusBulkDownloader [-h] --type {aut,abs,agg} [--urimongo URIMONGO] [--subjarea SUBJAREA] [--start START] [--end END]

Download Abstract and Authors from Scopus

optional arguments:
  -h, --help           show this help message and exit
  --type {aut,abs,agg}     aut => get authors from already downloaded abstracts, abs => get abstracts, agg => aggregate data
  --urimongo URIMONGO  MongoDB uri (default: mongodb://localhost:27017/)
  --subjarea SUBJAREA  Represents the subject area code associated with the content category desired (default: COMP)
  --start START        Start year for scrape (default: 1850)
  --end END            End year for scrape (default: 2007)
```

## Arguments

- `--type`: Specify the action to be performed. Use `aut` to get authors from already downloaded abstracts, or `abs` to get abstracts, or `agg` to aggregate data
- `--urimongo`: MongoDB URI for connecting to the database. If not provided, the default URI is `mongodb://localhost:27017/`.
- `--subjarea`: Represents the subject area code associated with the content category desired. The default value is `COMP`.
- `--start`: Start year to download abstracts . The default value is `1850`.
- `--end`: End year to download abstracts. The default value is `2007`.

## Examples

1. To get authors from already downloaded abstracts:

```
scopusBulkDownloader --type aut 
```

2. To get abstracts using the default parameters:

```
scopusBulkDownloader --type abs
```

3. To aggregate data:

```
scopusBulkDownloader --type agg
```

4. To get abstracts in the subject area `BIOC` from the year `2010` to `2021`:

```
scopusBulkDownloader --type abs --subjarea BIOC --start 2010 --end 2021
```

## Requirements

- Python >= 3.9
- Required Python packages (`pybliometrics`, `pymongo`, `pandas`, `pyspark`, etc.)
- MongoDB server

## License

This project is licensed under the [MIT License](LICENSE).