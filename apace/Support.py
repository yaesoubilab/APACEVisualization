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


def get_mean_interval(stat, interval_type='c', deci=0, form=None):
    """
    :param interval_type: 'c' for confidence interval, 'p' for percentile interval
    :param deci: digits to round the numbers to
    :param form: ',' to format as number, '%' to format as percentage, and '$' to format as currency
    :return: mean and percentile interval formatted as specified (if format is not specified, it returns (mean, PI)
    """

    if form is None:
        if interval_type == 'p':
            return stat.get_mean(), stat.get_PI(0.05)
        elif interval_type == 'c':
            return stat.get_mean(), stat.get_t_CI(0.05)
        else:
            raise ValueError('Invalid interval type.')
    else:
        return stat.get_formatted_mean_and_interval(
            interval_type=interval_type, alpha=0.05, deci=deci, form=form)

