# -*- coding: utf-8 -*-
from . import models
from . import wizard
from . import controller


# I have already done the report creating in pdf format. Next i need,
# Users can filter the report by the following criteria: member, checkout date, return date, book, category and genre.
# Sorting options should be provided for the report, allowing it to be sorted by both the checkout and due dates.
# If no filter is applied should return a report with the whole data.
# Report heading: Library Management Report
# headers: reference_id, ISBN, name, language, author, checkout date, return date, category, genre
# Use PSQL query to fetch data from the backend

