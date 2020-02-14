import csv
from datetime import date

import parameters


def write_to_csv(members):
    file_name = parameters.OUTPUT_FILE_NAME.format(date.today().strftime("%d-%m-%Y"))

    with open(file_name, mode='w+') as members_file:
        writer = csv.DictWriter(members_file, fieldnames=parameters.fieldnames)
        writer.writeheader()
        writer.writerows(members)
