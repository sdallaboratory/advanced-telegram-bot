from datetime import datetime
from typing import Union


class DataFiltering:
    '''
    Simple auxiliary filtering class
    '''
    @staticmethod
    def dict_list_slice(dicts: list, columns: list) -> list:
        '''
        Slices list of dicts by given columns(keys)

        Parameters
        ----------
        dicts : list
            list of dicts
        columns : list
            column(keys) names

        Returns
        -------
        list
            list of dicts sliced by given keys
        '''
        if columns != []:
            for i, _ in enumerate(dicts):
                dicts[i] = { c:dicts[i][c] for c in columns }
            return dicts
        else:
            return dicts

    @staticmethod
    def cyrillic_to_latin(text: str) -> str:
        '''
        Changes all cyrllic letter to its latin analog

        Parameters
        ----------
        text : str
            text where you want to change cyrillic letters

        Returns
        -------
        str
            modified string
        '''
        sim_dict = {
            "А": "A", "Р": "P", "К": "K",
            "В": "B", "Т": "T",
            "С": "C", "Х": "X",
            "Е": "E", "О": "O",
            "Н": "H", "М": "M"
        }

        for sym in sim_dict.keys():
            text = text.replace(sym, sim_dict[sym])

        return text

    @staticmethod
    def timestamp_to_date(date: Union[str, int]) -> str:
        '''
        transforms timestamp date to Y-m-d H:M:S format

        Parameters
        ----------
        date : Union[str, int]
            timestamp string or int

        Returns
        -------
        str
            formatted date string in Y-m-d H:M:S format
        '''
        ts = int(date)
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        return str(date)
