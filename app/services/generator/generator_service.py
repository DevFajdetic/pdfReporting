import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from services.pdf import pdf_service

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
PLOT_DIR = 'plots'


class Generator:
    def generate_sales_data(self, month: int) -> pd.DataFrame:
        # Date range from first day of month until last
        # Use ```calendar.monthrange(year, month)``` to get the last date
        dates = pd.date_range(
            start=datetime(year=2020, month=month, day=1),
            end=datetime(year=2020, month=month,
                         day=calendar.monthrange(2020, month)[1])
        )

        # Sales numbers as a random integer between 1000 and 2000
        sales = np.random.randint(low=1000, high=2000, size=len(dates))

        # Combine into a single dataframe
        return pd.DataFrame({
            'Date': dates,
            'ItemsSold': sales
        })

    def plot(self, data: pd.DataFrame, filename: str) -> None:
        plt.figure(figsize=(12, 4))
        plt.grid(color='#F2F2F2', alpha=1, zorder=0)
        plt.plot(data['Date'], data['ItemsSold'],
                 color='#087E8B', lw=3, zorder=5)
        plt.title(f'Sales 2020/{data["Date"].dt.month[0]}', fontsize=17)
        plt.xlabel('Period', fontsize=13)
        plt.xticks(fontsize=9)
        plt.ylabel('Number of items sold', fontsize=13)
        plt.yticks(fontsize=9)
        plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
        return

    def construct(self):
        # Delete folder if exists and create it again
        try:
            shutil.rmtree(PLOT_DIR)
            os.mkdir(PLOT_DIR)
        except FileNotFoundError:
            os.mkdir(PLOT_DIR)

        # Iterate over all months in 2020 except January
        for i in range(2, 13):
            # Save visualization
            self.plot(data=self.generate_sales_data(month=i),
                      filename=f'{PLOT_DIR}/{i}.png')

        # Construct data shown in document
        counter = 0
        pages_data = []
        temp = []
        # Get all plots
        files = os.listdir(PLOT_DIR)
        # Sort them by month - a bit tricky because the file names are strings
        files = sorted(os.listdir(PLOT_DIR),
                       key=lambda x: int(x.split('.')[0]))
        # Iterate over all created visualization
        for fname in files:
            # We want 3 per page
            if counter == 3:
                pages_data.append(temp)
                temp = []
                counter = 0

            temp.append(f'{PLOT_DIR}/{fname}')
            counter += 1

        return [*pages_data, temp]

    def generate_pdf(self, fileName):
        print(fileName)
        december = self.generate_sales_data(month=12)
        self.plot(data=december, filename='december.png')
        plots_per_page = self.construct()
        plots_per_page
        pdf = pdf_service.PDF()

        for elem in plots_per_page:
            print(elem)
            pdf.print_page(elem)
        
        fullFileName = fileName + '.pdf'
        pdf.output(os.path.join('products', fullFileName), 'F')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Generator.generate_sales_data(month=3)
    december = Generator.generate_sales_data(month=12)
    Generator.plot(data=december, filename='december.png')
    plots_per_page = Generator.construct()
    plots_per_page
    pdf = pdf_service.PDF()

    for elem in plots_per_page:
        pdf.print_page(elem)

    pdf.output('products/SalesReport.pdf', 'F')
