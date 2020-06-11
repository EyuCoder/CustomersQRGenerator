# qrcode-labelmaker

Printer: Brother QL-500

Label Size: 62x29mm

## Installation
Get Python 3

```
pip install -r requirements.txt
```

## Usage:
Generate Badge for all Customers: 
```
./QRGenerator.py --all
```

Generate Badge for a single Customers: 
```
./QRGenerator.py --single
```
#Customers Contract Number: `0000233`

Generate Badge starting from last Generator Customers Batch: 
```
./QRGenerator.py --from
```
#last Generated Contract Number: `0034755`
If you add the `--printer` switch, the label will automatically get printed
after creating. We asume that the printer is called *Brother_QL-500*.

The label is also saved as *label.pdf* in the root of this project.
