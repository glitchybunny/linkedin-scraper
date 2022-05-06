import json
import csv

if __name__ == '__main__':
    with open('output.json', 'r') as file:
        DATA = json.load(file)

    # Get max length of each section
    max_len_exp = 0
    max_len_vol = 0
    max_len_edu = 0
    for i in DATA:
        len_exp = len(DATA[i]["Experience"])
        if len_exp > max_len_exp:
            max_len_exp = len_exp
        len_vol = len(DATA[i]["Volunteering"])
        if len_vol > max_len_vol:
            max_len_vol = len_vol
        len_edu = len(DATA[i]["Education"])
        if len_edu > max_len_edu:
            max_len_edu = len_edu

    # Generate header rows of CSV
    row1 = [None, None, None, None]
    row1.append('Experience')
    for i in range(max_len_exp * 4 - 1):
        row1.append(None)
    row1.append('Volunteering')
    for i in range(max_len_vol * 4 - 1):
        row1.append(None)
    row1.append('Education')
    for i in range(max_len_edu * 4 - 1):
        row1.append(None)

    row2 = ['URL', 'Name', 'Title', 'About']
    for i in range(max_len_exp + max_len_vol + max_len_edu):
        row2.append('Title')
        row2.append('Subtitle')
        row2.append('Dates')
        row2.append('Description')

    # Write to CSV
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, escapechar='\\')
        writer.writerow(row1)
        writer.writerow(row2)

        # Loop through DATA and generate rows
        for i in DATA:
            row = [i, DATA[i]['Name'], DATA[i]['Title'], DATA[i]['About']]

            # Experience
            for j in DATA[i]['Experience']:
                for k in j.keys():
                    if j[k] == None:
                        row.append(None)
                    else:
                        row.append(j[k])
            for _ in range((max_len_exp - len(DATA[i]['Experience'])) * 4):
                row.append(None)

            # Volunteering
            for j in DATA[i]['Volunteering']:
                for k in j.keys():
                    if j[k] == None:
                        row.append(None)
                    else:
                        row.append(j[k])
            for _ in range((max_len_vol - len(DATA[i]['Volunteering'])) * 4):
                row.append(None)

            # Education
            for j in DATA[i]['Education']:
                for k in j.keys():
                    if j[k] == None:
                        row.append(None)
                    else:
                        row.append(j[k])
            for _ in range((max_len_edu - len(DATA[i]['Education'])) * 4):
                row.append(None)

            writer.writerow(row)
