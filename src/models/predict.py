import pandas as pd
from sklearn.ensemble import RandomForestClassifer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer
import logging

LOG_FILE = '../../logs/predict0.log'

logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE,
                    filemode='w', level=logging.INFO)
log = logging.getLogger(__name__)


def read_data(filename):
    df = pd.read_csv(filename)
    return df


def train_classifier(clf, X, y):
    ''' Fits a classifier to the training data. '''

    # Start the clock, train the classifier, then stop the clock
    start = time()
    f1_scorer = make_scorer(f1_score, pos_label='yes')
    # splits data and runs classifier on mutltiple splits of training data
    scores = cross_val_score(clf, X, y, f1_scorer, cv = 4)
    end = time()

    # Print the results
    print 'cross_val_score', scores
    print "Trained model in {:.4f} seconds".format(end - start)


def predict_labels(clf, features):
    ''' Makes predictions for kaggle's test set
        using a fit classifier based on F1 score.
    '''

    # Start the clock, make predictions, then stop the clock
    start = time()
    y_pred = clf.predict(features)
    end = time()

    # Print and return results
    print "Made predictions in {:.4f} seconds.".format(end - start)
    return y_pred


def write_labels(test, predictions, write_file):
    pred_df = pd.DataFrame(predictions)
    labels = test['ad_id'].merge(pred_df)
    labels.to_csv(write_file)


if __name__ == "__main__":
    train_file = ''
    data = read_data(train_file)
    y = train['clicked']
    X = train.drop('clicked', axis=1)

    clf = RandomForestClassifer()
    train_classifier(clf, X, y)

    # predict labels for kaggle's test data
    kaggle_test_file = ''
    write_file = ''
    test = read_data(test_file)
    predictions = predict_labels(clf, test)
    write_labels(test, predictions)
