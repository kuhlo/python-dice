"""A library for parsing and evaluating dice notation."""

from __future__ import absolute_import, print_function, unicode_literals

from pyparsing import ParseException
from dice.elements import TooManyDice

import dice.elements
import dice.grammar
import dice.utilities

__all__ = ['roll', 'roll_min', 'roll_max', 'ParseException', 'TooManyDice']
__author__ = ("Sam Clements <sam@borntyping.co.uk>, "
              "Caleb Johnson <me@calebj.io>")
__version__ = '1.2.0'


def roll(string, **kwargs):
    """Parses and evaluates a dice expression"""
    return _roll(string, **kwargs)


def roll_min(string, **kwargs):
    """Parses and evaluates the minimum of a dice expression"""
    return _roll(string, force_extreme=dice.elements.EXTREME_MIN, **kwargs)


def roll_max(string, **kwargs):
    """Parses and evaluates the maximum of a dice expression"""
    return _roll(string, force_extreme=dice.elements.EXTREME_MAX, **kwargs)


def parse_expression(string):
    return dice.grammar.expression.parseString(string, parseAll=True)


def _roll(string, single=True, raw=False, **kwargs):
    ast = parse_expression(string)
    elements = list(ast)
    result = [element.evaluate_cached(**kwargs) for element in elements]

    ret = elements if raw else result

    if single:
        return dice.utilities.single(ret)

    return ret
