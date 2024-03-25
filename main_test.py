# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import sys
from difflib import SequenceMatcher

EXCLUDING_RUNTYPE = ['R2R_HSU', 'R2R_test']
CSV_PATH = './design_list_PT_cleaned.csv'

SWITCH = None  # ['LOGO', 'intel', 'S3']

# Exclamatory signs to be removed
signs_to_remove = ['!', '!!', '#', '\n', '\t']

# Create a translation table
translation_table = str.maketrans('', '', ''.join(signs_to_remove))
MUST_SWITCHES = ['logo', 'project', 'block_name', 'scenario', 'run_type']
IMP_SWITCHES = ['logo', 'run_type']


def read_csv():
    pass

def keyword_pp(raw_keyword):
    updt_keyword = raw_keyword.lower()
    updt_keyword = updt_keyword.replace('#', '')
    # Create a translation table
    updt_keyword = updt_keyword.translate(translation_table)
    updt_keyword = updt_keyword.strip()
    return updt_keyword


def clean_df():
    raw = pd.read_csv(os.path.abspath(CSV_PATH))
    cols = list(raw.columns)
    # print(cols)
    updt_cols = {col: keyword_pp(col) for col in cols}
    upd_df = raw.rename(columns=updt_cols)
    switch_list = [keyword_pp(col) for col in cols]
    # switch_list = list(upd_df.columns)
    object_columns = upd_df.select_dtypes(include=['object'])
    pp_df = upd_df.copy()
    for col in object_columns:
        pp_df[col] = upd_df[col].apply(preprocess_text)
    return pp_df


# Function to preprocess text in each cell

def preprocess_text(cell):
    return cell.strip()

def take_input_from_options(options):
    while True:
        print("Choose one of the following options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Enter your choice (1-" + str(len(options)) + "): ")

        # Check if input is a valid integer
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)

        # Check if input is within the range of options
        if choice < 1 or choice > len(options):
            print("Invalid choice. Please enter a number between 1 and", len(options))
            continue

        return options[choice - 1]



def read_switch():

    raw = pd.read_csv(os.path.abspath(CSV_PATH))
    # raw = clean_df()
    cols = list(raw.columns)
    # print(cols)
    updt_cols = {col: keyword_pp(col) for col in cols}
    upd_df = raw.rename(columns=updt_cols)
    # switch_list = [keyword_pp(col) for col in cols]
    switch_list = list(upd_df.columns)
    return upd_df, switch_list, cols

def help():
    # TODO: Add Help statement
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your program.')

    # Add command-line arguments
    parser.add_argument('--option1', help='Description of option 1')
    parser.add_argument('--option2', help='Description of option 2')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Your program logic goes here
    print("Option 1:", args.option1)
    print("Option 2:", args.option2)

def combination_creator(arg_list):
    arg_dict = {}
    flag = 0
    value_list = []
    temp_key=None
    for arg in arg_list[1:]:
        if arg.startswith('-'):
            temp_key = arg[1:].replace('-','')
            arg_dict[temp_key] = list()
        else:
            if temp_key is not None:
                arg_dict[temp_key].append(arg)  # .lower()

    # print(arg_dict)
    for key in arg_dict.keys():
        if len(arg_dict[key]) > 1:
            print(f'WARNING: Please provide single arg for switch {key}.\nProvided arguments {arg_dict[key]}')
            sys.exit(1)
    for key in MUST_SWITCHES:
        if key not in arg_dict:
            print(f'WARNING: Please provide arguments for switch {key}.')
            sys.exit(1)

    return arg_dict

def find_closest_keyword(input_keyword, keyword_list):
    similarity_scores = [(keyword, SequenceMatcher(None, input_keyword, keyword).ratio()) for keyword in keyword_list]
    closest_keyword, similarity = max(similarity_scores, key=lambda x: x[1])
    return closest_keyword, similarity
def switch_check(arg_dict, switch):
    status = True
    for key in arg_dict.keys():
        if key not in switch:
            closest_keyword, _ = find_closest_keyword(key, switch)
            print(f"WARNING: switch '{key}' is not available in db")
            print('Closest matching switches are :', closest_keyword)
            print('Please enter a right or available switch')
            status = False
            sys.exit(1)
    return status


def dynamic_filter(arg_dict):
    try:
        eval_condition = True
        # for key in arg_dict:
        #     value = arg_dict[key][0]
        #     # Evaluate the filter condition dynamically
        #     filter_condition = f"row['{key}'] == {value}"
        #     eval_condition = eval_condition and eval(filter_condition)
        conditions = []
        for key in arg_dict.keys():
            value = arg_dict[key][0]
            # Evaluate the filter condition dynamically
            filter_condition = f"{key} == '{value}'"
            conditions.append(filter_condition)
        # print(conditions)
        condition_statement = " & ".join(conditions)
        # print(condition_statement)
        return condition_statement
        # eval_condition = all(eval(condition, {'row': row,  **row.to_dict()}) for condition in conditions)
        # return eval_condition
    except (KeyError, TypeError):
        # Handle potential errors (e.g., invalid column name)
        return False
def matching_check(df, arg_dict):
    # print(df.columns)
    # filtered_df = df[df.apply(lambda row: dynamic_filter(row, arg_dict), axis=1)]
    # df[MUST_SWITCHES] = df[MUST_SWITCHES].apply(lambda x: x.str)  # .lower()
    filtered_df = df.query(dynamic_filter(arg_dict))
    return filtered_df

def revised_input(input_dict, df):
    for val in IMP_SWITCHES:
        uniq_values = [val for val in df[val].unique() if (not pd.isnull(val)) and (not val.startswith('#'))]
        print(f'\nDo you mean any of these available values for {val}: \n')
        chosen_option = take_input_from_options(uniq_values + ['NOT AVAILABLE IN THE LIST'])
        if chosen_option != 'NOT AVAILABLE IN THE LIST':
            input_dict[val][0] = chosen_option
        else:
            input_dict[val][0] = input(f'Enter new input for switch "{val}": ')

    return input_dict

def check_runtype(arg_dict):
    if arg_dict['run_type'][0] in EXCLUDING_RUNTYPE:
        # TODO: Add message
        print('This check need extra........................')
        sys.exit(1)
def launcher():
    # TODO:
    # Check if the correct number of command-line arguments is provided
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <argument>")
    #     # sys.exit(1)

    # Access the command-line argument
    input_dict = ['-user']
    argument = sys.argv
    # print('argument', argument)

    if '-h' in argument or '--help' in argument:
        help()
    else:
        if SWITCH is None:
            updt_df, switch, raw_cols = read_switch()
            print(switch)
            # print('INFO: Available switches from the csv : ', switch)
        else:
            updt_df, _, raw_cols = read_switch()
            switch = SWITCH
            print('INFO: Available switches predefined : v', switch)
        # print('switch', switch)
        arg_dict = combination_creator(argument)
        # print('arg_dict', arg_dict)
        status = switch_check(arg_dict, switch)
        # print(f'arg_dict: {arg_dict}')

        if status:
            sub_df = matching_check(updt_df, arg_dict)
            count = sub_df.shape[0]

            print('\n')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            # print('\n')
            if count > 0:
                # print(f'Number of matching cases found: {count}')
                print('\nINFO: This test already exists and is not being added again.')
                # print('\n')
                sub_df_temp = sub_df.to_dict()
                for key in sub_df_temp.keys():
                    print(f'\n{key} : {sub_df_temp[key][0]}')

            else:
                print('\nINFO:No matching test cases found.')  #  \n Please enter the inputs')
                revised_arg_dict = revised_input(arg_dict, updt_df)
                check_runtype(revised_arg_dict)
                sub_df = matching_check(updt_df, revised_arg_dict)
                count = sub_df.shape[0]
                if count > 0:
                    print('\nINFO: This revised test already exists and is not being added again.')
                    # print('\n')
                    sub_df_temp = sub_df.to_dict()
                    for key in sub_df_temp.keys():
                        print(f'\n{key} : {sub_df_temp[key][0]}')
                else:
                    print('\nINFO:No matching test cases found for revised query : \n')
                    for key in revised_arg_dict.keys():
                        print(f'{key} : {revised_arg_dict[key][0]}')
                    print('\nPlease enter the inputs for new test: \n')
                    new_dict = {}
                    for sw in switch:
                        if sw in revised_arg_dict:
                            default_val = arg_dict[sw][0]
                            # uniq_values = updt_df[sw].unique()
                            # print(f'Enter input for switch "{sw}"\n')
                            # chosen_option = take_input_from_options(uniq_values)
                            # print(f'chosen input: {chosen_option}')
                            # new_dict[sw] = chosen_option
                            if sw not in IMP_SWITCHES:
                                new_dict[sw] = [input(f'Enter input for switch "{sw}" (or press enter for "{default_val}"): ') or default_val]
                            else:
                                new_dict[sw] = default_val
                        else:
                            new_dict[sw] = [input(f'Enter input for switch "{sw}": ')]
                    new_df = pd.DataFrame(new_dict)
                    modified_df = pd.concat([updt_df, new_df])

                    modified_df = modified_df.rename(columns= dict(zip(switch, raw_cols)))
                    modified_df.to_csv('design_list_PT_cleaned.csv', index=False)
        # if '--logo' in argument:
        #     logo_arg = input('Input logo arguments: ')
        #     print('Thanks for ur ip')
        #     print('logo arg are :', logo_arg)

        # Your program logic goes here
        # print("Command-line argument:", argument)


import argparse



def arparn_temp():
    print('heheheh')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    launcher()
