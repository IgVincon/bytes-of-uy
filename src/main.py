#!/usr/bin/env python # Keep only if intended to be executed as main.py
"""This is the entry point for an ETL pipeline."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from etl import extract_cuti

def main() -> None:
    extract_cuti.extract()
    # None #placeholder para evitar que indique error

if __name__ == "__main__":
    main()