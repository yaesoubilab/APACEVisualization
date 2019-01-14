import SimPy.PartialRankCorrelation as PRC
import SimPy.InOutFunctions as IO

# read outputs
daly_cost = IO.read_csv_cols(file_name='csvfiles/PartialRankCorrelation/TBOutputs0.csv',
                             n_cols=2,
                             if_ignore_first_row=True,
                             delimiter=',',
                             if_convert_float=True)

# read parameter samples
parameter_values = IO.read_csv_cols_to_dictionary(
    file_name='csvfiles/PartialRankCorrelation/TBParms0.csv',
    delimiter=',',
    if_convert_float=True)

# partial rank correlation for DALY
prc = PRC.PartialRankCorrelation(parameter_values=parameter_values,
                                 output_values=daly_cost[0])

prc.export_to_csv(file_name='PRC-DALY.csv',decimal=4)

# partial rank correlation for COST
prc = PRC.PartialRankCorrelation(parameter_values=parameter_values,
                                 output_values=daly_cost[1])

prc.export_to_csv(file_name='PRC-Cost.csv',decimal=4)