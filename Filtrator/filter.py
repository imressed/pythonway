# -*- coding: utf-8 -*-
__author__ = 'imressed'


import time

#: window_time in seconds
#: levenshtein_distance in steps

def levenshtein_distance(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1) # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = (previous_row[j] + 1, current_row[j - 1] + 1,
                                   previous_row[j - 1])
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


class PlateFilter(object):
    """Class for filtering car number using levenshtein algorithm"""
    def __init__(self, levenshtein_distance, window_time):
        self.lev_distance = levenshtein_distance
        self.window_time = window_time
        self.numbers = {}

    def add_number(self, num, timestamp):
        self.numbers[num] = timestamp

    def get_numbers(self):
        return self.numbers

    def del_number(self, key):
        del self.numbers[key]

    #: TODO: rewrite
    def clean_dict(fn):
        def wrapped(self, result):
            self.timestamp = time.time()
            for key, value in self.numbers.items():
                if abs(self.timestamp - value) > self.window_time:
                    self.del_number(key)
            return fn(self, result)
        return wrapped

    @clean_dict
    def _return(self, result):
        return result

    def check_number(self, number):
        self.number = number
        self.timestamp = time.time()
        self.add_fl = True
        for key, value in self.numbers.iteritems():
            if levenshtein_distance(self.number, key) <= self.lev_distance:
                if abs(self.timestamp - value) <= self.window_time:
                    self.add_fl = False
        self.numbers[self.number] = self.timestamp
        if self.add_fl:
            return self._return(True)
        else:
            return self._return(False)