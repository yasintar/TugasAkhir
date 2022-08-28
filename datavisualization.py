import argparse
from matplotlib import dates as mpl_date
import matplotlib.pyplot as plt
import pandas as pd

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file to visualize")
    parser.add_argument("-c", "--cpu", help="to get cpu stat visual", action="store_true")
    parser.add_argument("-r", "--ram", help="to get ram stat visual", action="store_true")
    parser.add_argument("-d", "--disk", help="to get internal storage stat visual", action="store_true")

    args = parser.parse_args()
    data = pd.read_csv(args.file)

    data['Time'] = pd.to_datetime(data['Time'])

    if(args.cpu):
        plt.plot_date(data['Time'], data['CPU_Precentage'])
    elif(args.ram):
        plt.plot_date(data['Time'], data['RAM_Precentage'])
    elif(args.disk):
        plt.plot_date(data['Time'], data['Disk_Precentage'])
    
    plt.gcf().autofmt_xdate()

    date_format = mpl_date.DateFormatter('%H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.tight_layout()

    plt.show()