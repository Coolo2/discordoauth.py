
import typing

def append_if_doesnt_exist(array : list, appendable : typing.Any, parameter : str) -> list:

    exists = False
    for item in array:
        if getattr(appendable, parameter) == getattr(item, parameter):
            exists = True 
    
    if not exists:
        array.append(appendable)
    
    return array

def item_by_value(array : list, parameter : str, value : typing.Any):
    exists = None
    for item in array:
        if getattr(item, parameter) == value:
            exists = item 
    
    return exists