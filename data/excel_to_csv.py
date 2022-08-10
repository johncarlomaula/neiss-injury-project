# DESCRIPTION: This script converts the NEISS excel files into csv files.
# To use this script, store the excel files in a folder named 'xldata'.
# Change the years in the code below if necessary.

# Import requied packages
import pandas as pd
import mock
from openpyxl.reader import excel
from os import listdir

# Fix error ragarding excel reader
with mock.patch.object(excel.ExcelReader, 'read_properties', lambda self: None):

    # Get list of excel file names
    file_names = [f for f in listdir('xldata') if not f.startswith('.')]

    # Check years
    for year in range(2017, 2022, 1):

        # Iterate through excel files
        for file in file_names:

            # Check year of the file
            if str(year) in file:

                # Read excel sheet
                dfs = pd.read_excel('xldata/' + file, sheet_name = None)

                # Iterate through sheets in the excel file
                for sheet in dfs.keys():

                    # Save data or FMT
                    if str(year) in sheet:
                        dfs[sheet].to_csv('data/' + sheet + '.csv', index = False, header = True)
                    else:
                        dfs[sheet].to_csv('data/'+ str(year) + '_' + sheet + '.csv', index = False, header = True)


