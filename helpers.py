from cornelia.imports import *

def display_opts(decimal_numbers=3,
                 max_rows=None,
                 max_cols=None):

    pd.options.display.float_format = ("{:." + str(decimal_numbers) + "f}").format
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.max_columns', max_cols)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

