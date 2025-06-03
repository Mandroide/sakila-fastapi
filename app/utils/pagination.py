import math


def calculate_page_number(offset: int, limit: int, total_elements: int) -> int:
    """Calculate the page number based on the given offset, limit, and total elements.

    Args:
        offset (int): The starting index of the current page (0-based).
        limit (int): The maximum number of elements per page.
        total_elements (int): The total number of elements across all pages.

    Raises:
        ValueError: If the limit is not a positive integer, or if the
            total elements is not a non-negative integer.

    Returns:
        int: The page number (1-based).
    """
    if limit <= 0:
        error_message = "Limit must be a positive integer."
        raise ValueError(error_message)

    if total_elements < 0:
        error_message = "Total elements must be a non-negative integer."
        raise ValueError(error_message)

    return math.ceil((offset - 1) / limit) + 1


def calculate_offset(page: int, page_size: int) -> int:
    """Calculate the offset of the current page based on the given page and page size."
    Args:
        page (int): The page number (0-based).
        page_size (int): The size of the current page (1-based).

    Returns:
        int: The offset of the current page (0-based).
    """
    if page_size <= 0:
        error_message = "Page size must be a positive integer."
        raise ValueError(error_message)
    return page * page_size


def calculate_total_pages(limit: int, total_elements: int) -> int:
    """Calculate the total number of pages based on the given offset, limit, and total elements.

    Args:
        limit (int): The maximum number of elements per page.
        total_elements (int): The total number of elements across all pages.

    Raises:
        ValueError: If the limit is not a positive integer,
            or if the total elements is not a non-negative integer.

    Returns:
        int: The total number of pages.
    """
    if limit <= 0:
        error_message = "Limit must be a positive integer."
        raise ValueError(error_message)

    if total_elements < 0:
        error_message = "Total elements must be a non-negative integer."
        raise ValueError(error_message)

    return math.ceil(float(total_elements) / limit)
