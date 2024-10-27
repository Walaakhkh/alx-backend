#!/usr/bin/env python3
"""
Module for paginating a dataset of popular baby names.
"""

import csv
from typing import List, Tuple, Dict, Any
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end indexes for pagination based on page and
    page_size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page from the dataset based on the specified page and page_size.

        Args:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            List[List]: A list of rows for the specified page of the dataset.
        """
        # Verify that both page and page_size are positive integers
        assert isinstance(page, int) and page > 0, (
            "page must be a positive integer"
        )
        assert isinstance(page_size, int) and page_size > 0, (
            "page_size must be a positive integer"
        )

        # Calculate start and end indexes for the requested page
        start_index, end_index = index_range(page, page_size)

        # Load the dataset if it hasn't been loaded already
        dataset = self.dataset()

        # Check if the start index is within the dataset range
        if start_index < len(dataset):
            return dataset[start_index:end_index]
        return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a hypermedia pagination dictionary for the specified page and
        page_size.

        Args:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing pagination details.
        """
        data = self.get_page(page, page_size)

        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': total_pages
        }
