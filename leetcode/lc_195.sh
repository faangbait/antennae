#!/bin/bash -e
# awk 'NR == 10 { print }' $1
awk 'NR>10 { exit } NR == 10 { print }' $1
