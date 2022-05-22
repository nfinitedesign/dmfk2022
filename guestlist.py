import ftplib
import logging
import mysql.connector
import settings

questions = {2: "number",
             8: "dont_show",
             9: "city",
             10: "company",
             11: "nick"}

logging.basicConfig(filename=settings.filename_log,
                    filemode='a',
                    format='%(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y - %H:%M:%S',
                    level=logging.DEBUG)

# connect to mysql database
conn = None
data = {}
try:
    conn = mysql.connector.connect(host=settings.sql_hostname,
                                   database=settings.sql_database,
                                   user=settings.sql_username,
                                   password=settings.sql_password)
    if conn.is_connected():
        logging.info(f'MySQL connection: OK (Host/Database: {settings.sql_hostname}/{settings.sql_database})')

        # read data from query
        cursor = conn.cursor()
        cursor.execute('select answer, question_id, pretixbase_orderposition.order_id from pretixbase_questionanswer '
                       'inner join pretixbase_orderposition on pretixbase_questionanswer.orderposition_id = pretixbase_orderposition.id '
                       'inner join pretixbase_orderpayment on pretixbase_orderposition.order_id = pretixbase_orderpayment.order_id '
                       'where question_id in (2, 8, 9, 10, 11) and pretixbase_orderpayment.state = "confirmed" order by pretixbase_orderposition.order_id desc;')

        row = cursor.fetchone()
        while row is not None:
            if not row[2] in data:
                data[row[2]] = {}
            data[row[2]][questions[row[1]]] = row[0]
            row = cursor.fetchone()
        logging.info(f'MySQL read: Number of entries: {len(data)})')

except BaseException as err:
    logging.error(f"MySQL read: Unexpected {err}, {type(err)}")
    exit(0)

finally:
    if conn is not None and conn.is_connected():
        conn.close()


# put data into html table
html_table = ''
for guest in data.keys():
    entry = data[guest]
    for field in ['number', 'nick', 'city', 'company']:
        if field not in entry:
            entry[field] = ''
    if entry["dont_show"] == 'False':
        html_table += f"<tr><td>{entry['number']}</td><td>{entry['nick']}</td><td>{entry['city']}</td><td>{entry['company']}</td></tr>\n"

# put html table into template
try:
    with open(settings.filename_tml, 'r') as file:
        html_data = file.read()
        html_data = html_data.replace('<GUESTLIST>', html_table)

    with open(settings.filename_web, 'w') as file:
        file.write(html_data)
    logging.info(f'HTML write: {settings.filename_dat} (Number of entries: {len(data)})')

except BaseException as err:
    logging.error(f"HTML write: Unexpected {err}, {type(err)}")
    exit(0)

# upload output to web server
try:
    ftp_server = ftplib.FTP_TLS(settings.ftp_hostname, settings.ftp_username, settings.ftp_password)
    ftp_server.encoding = "utf-8"

    with open(settings.filename_web, "rb") as file:
        ftp_server.prot_p()
        ftp_server.cwd("/html/dmfk2022")
        ftp_server.storbinary(f"STOR {settings.filename_web}", file)
    ftp_server.quit()
    logging.info(f'FTP Upload: Upload OK ({settings.filename_web}).')

except BaseException as err:
    logging.error(f"FTP upload: Unexpected {err}, {type(err)}")
    exit(0)
