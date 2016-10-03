import csv
import time

def read_csv(csv_file):
    csvfile = open(csv_file, 'rt')
    dictofdata = csv.DictReader(csvfile, delimiter=',')
    csvfile.close()
    data = [[row['OutcomeType'], row['OutcomeSubtype'], row['AnimalType'], row['SexuponOutcome'], row['AgeuponOutcome'], row['Breed'], row['Color']] for row in dictofdata]
    return data


def discretize_ageuponoutcome(data):
    for i in range(len(data)):
        if data[i][4] is not '' and ' ':
            num_date = int(data[i][4][0])

            if 'year' or 'years' in data[i][4]:
                data[i][4] = num_date * 365
            elif 'month' or 'months' in data[i][4]:
                data[i][4] = num_date * 30
            elif 'weeks' or 'week' in data[i][4]:
                data[i][4] = num_date * 7
            elif 'day' or 'days' in data[i][4]:
				data[i][4] = num_date * 1


def write_csv_file(csv_file, data):
	with open(csv_file, 'wt') as outcsv:
		writer = csv.DictWriter(outcsv, fieldnames = ["OutcomeType", "OutcomeSubtype", "AnimalType", "SexuponOutcome", "AgeuponOutcome", "Breed", "Color"])
		writer.writeheader()

		writer.writerows({'OutcomeType': row[0], 'OutcomeSubtype': row[1], 'AnimalType': row[2], 'SexuponOutcome': row[3],
							'AgeuponOutcome': row[4], 'Breed': row[5], 'Color': row[6]} for row in data)


#if __name__ == "__main__":
#   data = read_csv('train.csv')
#	discretize_ageuponoutcome(data)
#	write_csv_file('new_train.csv', data)
