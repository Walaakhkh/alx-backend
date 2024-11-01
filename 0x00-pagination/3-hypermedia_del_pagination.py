#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Get a hypermedia pagination dictionary for a dataset indexed by
        position.

        Args:
            index (int): The starting index for the current page.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary containing pagination details.
        """
        # Validate the index
        assert index >= 0 and index < len(self.__indexed_dataset), (
            "Index is out of range"
        )

        # Prepare the result dictionary
        result = {
            'index': index,
            'page_size': page_size,
            'data': [],
            'next_index': index + page_size
        }

        # Fetch the indexed dataset
        indexed_data = self.indexed_dataset()

        # Collect the data for the requested page
        current_index = index
        while len(result['data']) < page_size:
            if current_index in indexed_data:
                result['data'].append(indexed_data[current_index])
            current_index += 1
            # Handle the case where we run out of valid indexed entries
            if current_index >= len(indexed_data):
                break

        # Set the next_index in the result
        result['next_index'] = (
            current_index if current_index < len(indexed_data) else None
        )

        return result
