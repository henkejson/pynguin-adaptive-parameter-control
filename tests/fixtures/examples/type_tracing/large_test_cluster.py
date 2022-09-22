#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2022 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
# Simulate a large test cluster.
from dataclasses import dataclass

for i in range(100):
    exec(
        f"""
class Foo{i}:
    attribute_{i} = {i}

    def __init__(self):
        pass


class Bar{i}:
    attribute_{i} = {100 - i}

    def __init__(self):
        pass"""
    )


@dataclass
class Square:
    a: float


@dataclass
class Circle:
    r: float


@dataclass
class Triangle:
    h: float
    b: float
