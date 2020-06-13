# Customers QRCode Generator

Label Size: A4

## Installation
Get Python 3

```
pip install -r requirements.txt
```

## Usage:

create destination directories:

```
\cust_pdf
\cust_qr
```

Generate Badge for all Customers: 
```
QRGenerator.py --all

Customers kebele: 1
```

Generate Badge for a single Customers: 
```
QRGenerator.py --single

Customers kebele: 4

Customers Contract Number: 0000233
```


Generate Badge starting from last Generator Customers Batch: 
```
QRGenerator.py --from

Customers kebele: 7

last Generated Contract Number: 0034755
```

for more you can use `--help`
