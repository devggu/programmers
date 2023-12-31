import re
import pandas as pd

def update_loc(row: int, col: int, value: str, df: pd.DataFrame, merge_history: dict):
    df.at[row,col] = value
    if f"{row}_{col}" in merge_history.keys():
        for i in merge_history[f"{row}_{col}"]:
            df.at[i[0],i[1]] = value
        

def update_val(value1: str, value2: str, df: pd.DataFrame):
    df.replace(value1,value2,inplace=True)

def merge(row1: int, col1: int, row2: int, col2:int, df: pd.DataFrame, merge_history: dict ):
    merge_history[f"{row1}_{col1}"]=[[row2,col2]]
    merge_history[f"{row2}_{col2}"]=[[row1,col1]]
    
    df.at[row2,col2] = df.loc[row1,col1]
    

def unmerge(row,col,df,merge_history):
    pass


def print_out(row: int, col: int, df: pd.DataFrame):
    return df.loc(row,col)


def command_parser(command: str, df: pd.DataFrame, merge_history: dict):
    m = re.match(r"^(\w+).*$",command)
    if m.group(1) == "UPDATE":
        m = re.match(r"^UPDATE\s+(\d+)\s+(\d+)\s+([A-Za-z0-9]+)$",command)
        m2 = re.match(r"^UPDATE\s+([A-Za-z0-9]+)\s+([A-Za-z0-9]+)$",command)
        if m:
            row = m.group(1)
            col = m.group(2)
            value = m.group(3)
            update_loc(row,col,value,df,merge_history)
            
        elif m2:
            value1 = m2.group(1)
            value2 = m2.group(2)
            update_val(value1,value2,df,merge_history)     
    
    elif m.group(1) == "PRINT":
        m = re.match(r"^PRINT\s+(\d+)\s+(\d+)$",command)
        row = m.group(1)
        col = m.group(2)
        print_out(row,col,df)
        
    elif m.group(1) == "MERGE":
        m = re.match(r"^MERGE\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$",command)
        row1 = m.group(1)
        col1 = m.group(2)
        row2 = m.group(3)
        col2 = m.group(4)
        merge(row1,col1,row2,col2,df,merge_history)
        
    elif m.group(1) == "UNMERGE":
        m = re.match(r"^UNMERGE\s+(\d+)\s+(\d+)$",command)
        row= m.group(1)
        col= m.group(2)
        unmerge(row,col,df,merge_history)

    return 0


def solution(commands):
    df = pd.DataFrame()
    command_list = eval(commands)
    merge_history = {}
    for command in command_list:
        print(command)
        command_parser(command,df,merge_history)
    
    print(df)
    answer = []
    return answer


solution('["UPDATE 1 1 menu", "UPDATE 1 2 category", "UPDATE 2 1 bibimbap", "UPDATE 2 2 korean", "UPDATE 2 3 rice", "UPDATE 3 1 ramyeon", "UPDATE 3 2 korean", "UPDATE 3 3 noodle", "UPDATE 3 4 instant", "UPDATE 4 1 pasta", "UPDATE 4 2 italian", "UPDATE 4 3 noodle","MERGE 1 2 1 3"]')