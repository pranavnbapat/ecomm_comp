import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join
def new_plotting():
    # create a new directory for the output charts
    output_dir = "data/price_comparison_charts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    products_dir='products'
    product_files=os.listdir(products_dir)
    for f in product_files:
        new_folder = join(output_dir,f)
        os.makedirs(new_folder,exist_ok=True)
    product_files =[join(products_dir,i) for i in product_files]
    for folder in product_files:
        csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

        # iterate over each CSV file
        for file in csv_files:
            # read the CSV file into a pandas DataFrame
            file_path = join(folder,file)
            df = pd.read_csv(file_path)

            # create a box plot and line plot for the prices, grouped by source
            sns.lineplot(y="prices", data=df,x=df.index,hue='source').set(title='Price_comparison')


            # add text to the box plot to show the number of products from each source

            plt.legend(loc="best")

            plt.savefig(file_path.replace(products_dir,output_dir).replace(".csv", "_plot.jpg"))

            plt.close()
def old_plotting():
    # create a new directory for the output charts
    output_dir = "data/price_comparison_charts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    products_dir='products'
    product_files=os.listdir(products_dir)
    for f in product_files:
        new_folder = join(output_dir,f)
        os.makedirs(new_folder,exist_ok=True)
    product_files =[join(products_dir,i) for i in product_files]
    for folder in product_files:
        csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

        # iterate over each CSV file
        for file in csv_files:
            try:
                # read the CSV file into a pandas DataFrame
                file_path = join(folder,file)
                df = pd.read_csv(file_path)
                bol=['Bol']*len(df)
                amazon = ['Amazon']*len(df)
                bol.extend(amazon)
                new_df = pd.DataFrame({
                    'prices' : df['bol_price'].append(df['amazon_price']),
                    'source' : bol
                })
                # create a box plot and line plot for the prices, grouped by source
                sns.lineplot(y="prices", data=new_df,x=new_df.index,hue='source').set(title="Price Comparison")
                # add text to the box plot to show the number of products from each source
                plt.legend(loc="best")

                plt.savefig(file_path.replace(products_dir,output_dir).replace(".csv", "_plot.jpg"))
               # plt.show()
                plt.close()
            except:
                continue


if __name__=='__main__':
    old_plotting()