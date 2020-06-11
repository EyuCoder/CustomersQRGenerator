import pyqrcode
import png
import pyodbc
import os
import click
from tqdm import tqdm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

SQL_ALL = '''
        SELECT top(15) subscriber.name, subscriber.customerCode, subscription.serialNo, (SELECT [name]
        FROM [Main_2006].[dbo].[TransactionItems] where code=subscription.itemCode), subscription.modelNo, subscription.contractNo
        FROM subscriber INNER JOIN subscription ON subscriber.id=subscription.subscriberID  
        where Subscription.ticksTo=-1 order by subscription.contractNo'''
SQL_SINGLE = '''
        SELECT DISTINCT subscriber.name, subscriber.customerCode, subscription.serialNo, (SELECT [name]
        FROM [Main_2006].[dbo].[TransactionItems] where code=subscription.itemCode),subscription.modelNo, subscription.contractNo
        FROM subscriber INNER JOIN subscription ON subscriber.id=subscription.subscriberID  
        where Subscription.ticksTo=-1 and  subscription.contractNo='''
SQL_FROM = ''' '''

conn = pyodbc.connect(
    "Driver=SQL Server Native Client 11.0;"
    "Server=KINGSCXR\\SQLSERVER;"
    "Database=Subscriber;"
    "Trusted_Connection=Yes;"
)

@click.command()
@click.option('--all', '-a', help="Define the filename of the template to use")
@click.option('--single', '-s', help="Write the owner onto the label")

documentTitle = 'WSIS Water Meter QRCode!'

qr_dir = os.getcwd()+"\\cust_qr"
pdf_dir = os.getcwd()+"\\cust_pdf"



def generate_qrcode(contract_no):
    url = pyqrcode.create(contract_no)
    image_name = f"{qr_dir}\\qrcode-{contract_no}.png"
    url.png(image_name, scale=6)
    return image_name


def generate_pdf(customerName, customerCode, connectionNo, meterInfo, contract_no):
    file_name = os.path.join(qr_dir, f'qrcode-{contract_no}.png')
    pdf_name = f"{pdf_dir}\\qrcode-{contract_no}.pdf"
    
    pdf = canvas.Canvas(pdf_name)
    pdf.setTitle(documentTitle)

    pdf.setFont("Courier-Bold", 15)
    pdf.setFillColor(colors.black)

    pdf.drawString(150, 760, f'Customer Name: {customerName}')
    pdf.drawString(150, 730, f'Customer Code: {customerCode}')
    pdf.drawString(150, 700, f'Connection No: {connectionNo}')
    pdf.drawString(150, 670, f'Meter Info: ')

    pdf.setFont("Courier-Bold", 10)

    pdf.drawString(200, 640, f'Serial No: {meterInfo[1]}')
    pdf.drawString(200, 620, f'Item Code: {meterInfo[2]}')
    pdf.drawString(200, 600, f'Model No: {meterInfo[0]}')

    pdf.line(130, 590, 470, 590)

    # insert qrcode
    pdf.drawInlineImage(file_name, 180, 330, width=250, height=250)
    pdf.save()


# DBHandler
def load_customers(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    for row in tqdm(cursor, desc='Generating QR Codes', unit=' customers'):
        customers = str(row[0])
        # print(row[0] + row[1] + row[2] + row[3] + row[4])
        
        customerName = row[0]
        customerCode = row[1]
        connectionNo = row[5]
        meterInfo = [row[2], row[3], row[4]]
        contract_no = str(row[5])
        generate_pdf(customerName, customerCode, connectionNo, meterInfo, contract_no)

if __name__ == "__main__":
    load_customers(conn, SQL_ALL)
