import csv
def google_rank_rows():
    readfile = open('app/static/app/Copy of Harvard Network Matrix.xlsx - Copy of Sheet1.csv', 'r')
    reader = csv.DictReader(readfile)

    rows = []
    for row in reader:
        new_row = {}
        new_row['id'] = row['ID']
        new_row['Rank'] = row['Rank']
        new_row['Title'] = row['Title']
        new_row['Link'] = row['Link']
        new_row['Ranking'] = row['Ranking']
        links = []
        for i in range(22):
            if row[str(i+1)]=="1":
                links.append(str(i+1))
        new_row['Backlinks'] = links
        new_row['Backlink_info'] = []
        rows.append(new_row)

    for row in rows:
        for link in row['Backlinks']:
            id = int(link)
            rank = ""
            title = ""
            for roww in rows:
                if roww['id'] == str(id):
                    rank = roww['Rank']
                    title = roww['Title']
                    last = (link != row['Backlinks'][len(row['Backlinks'])-1])
                    row['Backlink_info'].append((rank,title, last))

    return rows
