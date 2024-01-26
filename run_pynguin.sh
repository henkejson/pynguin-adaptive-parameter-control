#!/bin/bash

pynguin \
--project-path input/ \
--output-path output/ \
--module-name bmi_calculator \
--maximum_search_time 20 \
--algorithm 'DYNAMOSA' \
-v
#--number_of_mutations 1 \
