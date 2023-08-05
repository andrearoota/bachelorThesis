from argparse import ArgumentParser
from scrapeAbstracts import AbstractDownloader
from scrapeAuthors import AuthorDownloader
from dotenv.main import load_dotenv
import os


SUBJAREA_DEFAULT = 'COMP'
YEAR_START_DEFAULT = 1850
YEAR_END_DEFAULT = 2007

def main ():
    parser = ArgumentParser(prog='scraperScopus', description='Scrape Abstract and Authors from Scopus')
    parser.add_argument('--type', type=str, choices=['aut', 'abs'], required=True, help='aut => get authors from already downloaded abstracts, abs => get abstracts')
    parser.add_argument('--subjarea', type=str, default=SUBJAREA_DEFAULT, help=f'Represents the subject area code associated with the content category desired (default: {SUBJAREA_DEFAULT})')
    parser.add_argument('--start', type=int, default=YEAR_START_DEFAULT, help=f'Start year for scrape (default: {YEAR_START_DEFAULT})')
    parser.add_argument('--end', type=int, default=YEAR_END_DEFAULT, help=f'End year for scrape (default: {YEAR_END_DEFAULT})')
    args = parser.parse_args()

    load_dotenv()

    if args.type == 'abs':
        obj = AbstractDownloader(start_year=args.start, end_year=args.end, subj_area=args.subjarea)
        obj.run()
    else:
        obj = AuthorDownloader(
            mongodb_read_uri=os.environ['MONGOBD_READ_URI'],
            mongodb_write_uri=os.environ['MONGOBD_WRITE_URI']
        )
        obj.download_authors_from_abstracts()

if __name__ == '__main__':
    main()
