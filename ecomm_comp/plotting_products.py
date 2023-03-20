import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join
import paramiko
import io


def setup_ec2():
    print("Connecting to EC2")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('3.69.255.112', username='ec2-user', key_filename='airflow-test-key.pem')
    print("Connection successful")
    return ssh


def get_data_ec2(ssh, remote_path):
    print("Reading CSV files from " + remote_path)
    stdin, stdout, stderr = ssh.exec_command('ls ' + remote_path + '/*.csv')
    file_list = [filename.strip() for filename in stdout.readlines()]
    # Loop over list of file names and read each CSV file into a pandas DataFrame
    df_list = []
    for filename in file_list:
        transport = ssh.get_transport()
        channel = transport.open_channel('session')
        channel.exec_command('cat ' + filename)
        file_obj = io.StringIO()
        for line in channel.makefile('r'):
            file_obj.write(line)
        file_obj.seek(0)
        df = pd.read_csv(file_obj)
        df_list.append(df)
        channel.close()
    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)
    return df


ssh = setup_ec2()
remote_path = '/home/ec2-user/ecomm/ecomm_comp/ecomm_comp/products/garmin_smartwatch_2023_03_12_17_13_22_clustered'
df = get_data_ec2(ssh, remote_path)
ssh.close()


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


def ec2_plotting(df):
    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 8))

    amazon_data = df[df['source'] == 'Amazon']
    bol_data = df[df['source'] == 'Bol']

    amazon_list = amazon_data["price"].to_list()
    bol_list = bol_data["price"].to_list()

    # Create a line plot
    sns.lineplot(amazon_list, label='Amazon')
    sns.lineplot(bol_list, label='Bol')

    # Add plot labels and titles
    plt.xlabel('Times')
    plt.ylabel('Price')
    plt.title('Price Variations Over Time')

    # Show the plot
    plt.show()


ec2_plotting(df)
