import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

MONTHS = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
    "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
}


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    evidence = []
    labels = []

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            evidence.append([
                int(row[0]),  # Administrative
                float(row[1]),  # Administrative_Duration
                int(row[2]),  # Informational
                float(row[3]),  # Informational_Duration
                int(row[4]),  # ProductRelated
                float(row[5]),  # ProductRelated_Duration
                float(row[6]),  # BounceRates
                float(row[7]),  # ExitRates
                float(row[8]),  # PageValues
                float(row[9]),  # SpecialDay
                MONTHS[row[10]],  # Month
                int(row[11]),  # OperatingSystems
                int(row[12]),  # Browser
                int(row[13]),  # Region
                int(row[14]),  # TrafficType
                1 if row[15] == "Returning_Visitor" else 0,  # VisitorType
                1 if row[16] == "TRUE" else 0  # Weekend
            ])
            labels.append(1 if row[17] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    true_positives = sum(1 for actual, predicted in zip(
        labels, predictions) if actual == predicted == 1)
    true_negatives = sum(1 for actual, predicted in zip(
        labels, predictions) if actual == predicted == 0)
    total_positives = labels.count(1)
    total_negatives = labels.count(0)

    sensitivity = true_positives / total_positives
    specificity = true_negatives / total_negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
