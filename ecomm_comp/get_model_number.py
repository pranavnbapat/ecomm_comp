import pandas as pd
import glob

path = "data"
extension = 'csv'

files = glob.glob(path + "/*." + extension)

for filename in files:
    # If file(s) found
    if filename:
        df = pd.read_csv(filename, index_col=None)

        # Get the link column of the file(s)
        links = df.link
        for i in links:
            # Open the link in BS4 and get the details
            # Model number for now and up to 5 images as some model numbers have different last few digits.
            # So, we might have to compare model numbers and images to get the exact match
            print(i)

            # Once details are retrieved, update the same CSV file with the new details

    break

