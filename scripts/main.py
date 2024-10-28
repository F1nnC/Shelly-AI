from scripts.data.get_conditions import check_last_update
from scripts.data.data_processing import data_processing


def main():
    
    check_last_update()
    data_processing()
