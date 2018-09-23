import csv
import numpy


def read_csv_cols(file_name, n_cols, if_ignore_first_row=True, delimiter=',', if_convert_float=False):
    """ reads the columns of a csv file
    :param file_name: the csv file name
    :param n_cols: number of columns in the csv file
    :param if_ignore_first_row: set True to ignore the first row
    :param delimiter: to separate by comma, use ',' and by tab, use '\t'
    :param if_convert_float: set True to convert column values to numbers
    :returns a list containing the columns of the csv file
    """
    with open(file_name, "r") as file:
        csv_file = csv.reader(file, delimiter=delimiter)

        # initialize the list to store column values
        cols = []
        for j in range(0, n_cols):
            cols.append([])

        # read columns
        for row in csv_file:
            for j in range(0, n_cols):
                if row[j] != "":
                    cols[j].append(row[j])

        # delete the first row if needed
        if if_ignore_first_row:
            for j in range(0, n_cols):
                del cols[j][0]

        # convert column values to float if needed
        if if_convert_float:
            for j in range(0, n_cols):
                try:
                    cols[j] = numpy.array(cols[j]).astype(numpy.float)
                except:
                    cols[j] = cols[j]

        return cols


def proper_file_name(text):
    """
    :param text: filename
    :return: filename where invalid characters are removed
    """
    return text.replace('|', ',').replace(':', ',').replace('<', 'l').replace('>', 'g')


def get_mean_PI(stat, deci, form):
    """
    :return: mean and percentile interval formatted as specified
    (if format is not specified, it returns (mean, PI)
    """

    if form is None:
        return stat.get_mean(), stat.get_percentile(0.05)
    else:
        return stat.format_estimate_PI(0.05, deci, form)
