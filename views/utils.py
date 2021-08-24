"""
Module for utils used by views.
"""
import os


def clear_screen():
    """
    Clears screen either on unix or windows system
    """
    os.system('cls||clear')
