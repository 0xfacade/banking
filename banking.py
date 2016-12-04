import os.path
from glob import glob
import csv
import codecs
import webbrowser

program_dir = os.path.dirname(os.path.realpath(__file__))

def get_csv_filename():
    downloads_dir = os.path.expanduser("~\\Downloads")
    os.chdir(downloads_dir)
    csv_files = glob("*.csv")
    csv_files = [(file, os.stat(file).st_ctime) for file in csv_files]
    newest = max(csv_files, key=lambda t: t[1])
    return newest[0]
    
def extract_data(csv_filename):
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = []
        for row in reader:
            if "Buchungstag" in row:
                break
            header.append(row)
        body = []
        for row in reader:
            body.append(row)
        return header, body

def extract_table_data(header, body):
    table_header = ["Buchungstag", "Wertstellung", "Umsatzdetails", "Soll", "Haben"]
    table = []
    for data in body:
        row = []
        row.append(data[0])
        row.append(data[1])
        row.append(data[2] + " " + data[3])
        row.append(data[-3])
        row.append(data[-2])
        table.append(row)
    return table_header, table

def extract_title(header):
    return "Kontoauszug " + str(header[1][0])

def generate_table_html(table_header, table):
    html = "<table class=\"table\"><tr>"
    for cell in table_header:
        html += "<th>" + cell + "</th>"
    html += "</tr>"
    for row in table:
        html += "<tr>"
        for cell in row:
            html += "<td>" + cell + "</td>"
        html += "</tr>"
    return html

def generate_html(header, body):
    os.chdir(program_dir)
    table_header, table_data = extract_table_data(header, body)
    table_html = generate_table_html(table_header, table_data)
    template = None
    with open("kontoauszug_template.htm") as template_file:
        template = template_file.read()

    template = template.replace("{{title}}", extract_title(header))
    template = template.replace("{{table}}", table_html)
    
    with open("kontoauszug.htm", "w") as output:
        output.write(template)
    
            
def main():
    csv_filename = get_csv_filename()
    header, body = extract_data(csv_filename)
    generate_html(header, body)
    webbrowser.open("kontoauszug.htm")

if __name__ == "__main__":
    main()
