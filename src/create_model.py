import sys
import pickle
import itertools as it

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from common import gc


key = '1_CsvRPqVPLqwDfMUJjHTQarFwp09IfPX7ON9pyFqxB0'
workbook = gc.open_by_key(key)
jobs_sheet = workbook.get_worksheet(0)


def get_rows():
    all_cols = [jobs_sheet.col_values(ndx) for ndx in (1, 2, 5, 3)]

    for row in it.islice(zip(*all_cols), 1, None):
        if all(not i for i in row):
            raise StopIteration()
        yield row


def train_model(all_jobs):
    rated_jobs = all_jobs.dropna()

    pos_examples = rated_jobs[rated_jobs.sounds_cool == 1]
    neg_examples = rated_jobs[rated_jobs.sounds_cool == 0].sample(pos_examples.shape[0])
    undersampled = pd.concat([pos_examples, neg_examples])

    X = undersampled['title'].as_matrix()
    y = undersampled['sounds_cool'].as_matrix()

    vect = CountVectorizer()
    Xp = vect.fit_transform(X).toarray()
    clf = LogisticRegression().fit(Xp, y)

    return clf, vect


if __name__ == '__main__':
    all_jobs = pd.DataFrame(data=list(get_rows()), columns=['title', 'company', 'sounds_cool', 'url'])
    all_jobs['sounds_cool'] = pd.to_numeric(all_jobs['sounds_cool'])
    clf, vect = train_model(all_jobs)

    clf_loc, vect_loc = sys.argv[1:3]
    with open(clf_loc, 'wb') as f:
        pickle.dump(clf, f)
    with open(vect_loc, 'wb') as f:
        pickle.dump(vect, f)
