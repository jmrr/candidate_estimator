import sys
import pandas as pd
from iso8601 import parse_date
from sklearn.metrics import accuracy_score
# from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


def main():
    # Features:
    #
    #   applicationId:  each candidate has multiple applications
    #                   for the video interview
    #
    #   candidateId:    candidate unique identifier
    #
    #   invitationDate: the time the candidate was invited
    #                   to take a video interview
    #
    #   isRetake:       True if the candidate was asked to
    #                   re-record their answer
    #
    #   speechToText:   the candidate’s answer as a JSON-serialized list of
    #                   dictionary of word strings;
    #                   e.g. {"name": "outgoing", "time": "5.43",
    #                   "duration": "0.64", "confidence": "0.870"}
    #                   represents that in this candidate’s answer,
    #                   the speech to text algorithm detected the word
    #                   “outgoing” at “"5.43” seconds into the video,
    #                   which the candidate took “0.64” seconds to say,
    #                   and the speech to text algorithm is “0.870” = 87%
    #                   confident that the candidate actually said this word
    #
    #   applicationTime: the time the candidate completed their video interview at
    #
    #   videoLength:    the video length of the candidate’s answer in seconds
    #
    #   score:         the score is hand labeled by a human, and it represents
    #                  the quality of the candidate’s answer per application.

    if len(sys.argv) != 2:
        print('Usage: python3 -m generate_model PATH_TO_DATA_FILE')
        return

    data = pd.read_csv(sys.argv[1])

    # timedelta: time (in seconds) spent by candidates to submit the application
    data['timedelta'] = data.apply(
        lambda row: (parse_date(row['applicationTime'])
                     - parse_date(row['invitationDate'])).seconds,
        axis=1
    )

    x = data[[
        'timedelta',
        'videoLength',
    ]]

    y = data[[
        'score',
    ]]

    x_train, x_test, y_train, y_test = train_test_split(x, y)
    model = MLPClassifier(
        solver='lbfgs',
        hidden_layer_sizes=(5, 3),
        alpha=0.001,
        random_state=1
    )
    # model = GaussianNB()
    # model = BernoulliNB()
    model.fit(x_train, y_train)

    y_prediction = model.predict(x_test)
    joblib.dump(model, 'model.pkl')

    print('Model accuracy score: {}'.format(
        accuracy_score(y_test, y_prediction)
    ))


if __name__ == '__main__':
    main()
