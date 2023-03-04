import pandas as pd

def main():
    tables = pd.read_html('https://livingwage.mit.edu/counties/10001')
    print(tables)

if __name__ == '__main__':
    main()