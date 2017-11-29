from oauth2client.service_account import ServiceAccountCredentials
import gspread
import itertools as it
import six

scope = ['https://spreadsheets.google.com/feeds']
filename = 'personal-etl-dba50f184134.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)

gc = gspread.authorize(credentials)

def pairwise(iterable):
    """ https://docs.python.org/2/library/itertools.html """
    a, b = it.tee(iterable)
    next(b, None)
    return six.moves.zip(a, b)
