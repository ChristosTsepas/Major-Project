# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 13:14:08 2023

@author: ctsepas
"""






import pandas as pd
from scipy import stats

def load_dti_metrics(left_excel_file): 
    # Load MD, FA, and error values from Excel into a DataFrame
    df = pd.read_excel(left_excel_file)
    
    
    # Rename columns for clarity
    df.columns = ['Mean FA', 'SD FA', 'Mean ADC (in mm^2/s)', 'SD ADC (in mm^2/s)' ]
     

    # Drop rows with NaN values
    df = df.dropna()
    
       
   # the excel will have two sets of data left and right. I want to read them and load the values in an excel
    

    # Convert FA, MD, and standard deviation values to numpy arrays for groups
    fa_left = df['Mean FA'].to_numpy()
    std_fa_left = df['STD_FA_left'].to_numpy()
    fa_right = df['FA_right'].to_numpy()
    std_fa_right = df['STD_FA_right'].to_numpy()
    md_left = df['MD_left'].to_numpy()
    std_md_left = df['STD_MD_left'].to_numpy()
    md_right= df['MD_right'].to_numpy()
    std_md_right = df['STD_MD_right'].to_numpy()


    return  fa_left, fa_right, md_left, md_right



def load_DKI_metrics():
    
    

def function_that_seperates_Groups_in_left_right_excel(left_excel, right_excel):
    
    # this functions reads the file names and returns the different groups
    # i want to seperate groups for both the two excel files (right_left) and then create different excels
    # excel one DTI_AP (and inside DTI_AP_left vs DTI_AP_right)
    # excel two DTI_PA (and inside DTI_PA_left vs DTI_PA_right)
    # excle three DTIADS_AP (...)
    # excel four DTIADS_PA
    # excel five NH_AP
    # excel six NH_PA    
    
    def save_data_to_excel(output_file, dti_ap, dti_pa, dti_ads_ap, dti_ads_pa, nh_ap, nh_pa):
        
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            
            # Write each DataFrame to the same sheet with different starting row
            dti_ap.to_excel(writer, sheet_name='Data', startrow=0, index=False)
            dti_pa.to_excel(writer, sheet_name='Data', startrow=len(dti_ap)+2, index=False)
            dti_ads_ap.to_excel(writer, sheet_name='Data', startrow=len(dti_ap)+len(dti_pa)+4, index=False)
            dti_ads_pa.to_excel(writer, sheet_name='Data', startrow=len(dti_ap)+len(dti_pa)+len(dti_ads_ap)+6, index=False)
            nh_ap.to_excel(writer, sheet_name='Data', startrow=len(dti_ap)+len(dti_pa)+len(dti_ads_ap)+len(dti_ads_pa)+8, index=False)
            nh_pa.to_excel(writer, sheet_name='Data', startrow=len(dti_ap)+len(dti_pa)+len(dti_ads_ap)+len(dti_ads_pa)+len(nh_ap)+10, index=False)





def perform_t_test(parameter_left, parameter_right ):
    
    
    # Define level of statistical significance
    alpha = 0.05 
  
    
    # Check normality using Shapiro-Wilk test for FA values
    stat_left, p_left = stats.shapiro(parameter_left)
    stat_right, p_right = stats.shapiro(parameter_right)

    # Print normality test results for FA values
    print(f'Shapiro-Wilk test for left ear FA: Statistic={stat_left}, p-value={p_left}')
    print(f'Shapiro-Wilk test for right ear FA: Statistic={stat_right}, p-value={p_right}')

    # Perform t-test only if FA data is approximately normally distributed
    if p_left > alpha and p_right > alpha:
        # Perform paired t-test with unequal variances
        t_statistic, p_value = stats.ttest_rel(parameter_left, parameter_right)

        # Print the results for the parameter
        print(f'T-statistic for {parameter_left}: {t_statistic}')
        print(f'P-value for {parameter_left}: {p_value}')

        if p_value_fa < alpha:
            print(f'Reject the null hypothesis for {parameter_left}. There is a significant difference between left and right ear {parameter_left}.')
        else:
            print(f'Fail to reject the null hypothesis for {parameter_left}. There is no significant difference between left and right ear {parameter_left}.')
    else:
        print(f'{parameter_left} data is not approximately normally distributed. Consider non-parametric tests or transformations.')


    





if __name__ == "__main__":
    # Replace 'path/to/your/excel/file.xlsx' with the path to your Excel file
    excel_file_left = r""
    excel_file_right = r""
    
    function_that_seperates_Groups_in_left_right_excel(left_excel, right_excel)
    
    
    fa_left, fa_right, md_left, md_right = load_dti_metrics()
    
    mk_left, mk_right, ak_left, ak_right, rk_left, rk_right = load_dki_metrics()
    
    apply_t_test(left_parameter, right_parameter)
   
       
 
