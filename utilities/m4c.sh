#!/bin/bash

################################################################################
# This script generates user-readable MAC Addresses. It's pretty useless.
#
# But it's a cool pattern.
#
# Usage: ./m4c.sh <wordlist>
# Wordlist: http://www.wordgamedictionary.com/twl06/download/twl06.txt
#
# The result looks like this:
#
# affec7ab1e
# affec71e55
# a5be5705e5
# a55e55ab1e
# baff1e9ab5
# ba9a7e11e5
# b1a570c0e1
# b1e55ede57
# b0b51edded
# b0071e99ed
# ...
################################################################################

WORDS=($(dos2unix < $1))

for WORD in "${WORDS[@]}"; do
  if [[ ${WORD} =~ ^[0-9A-Fa-fLlOoSsTtGg]{10}$ ]]; then
    echo ${WORD} | \
      sed -r 's/[Ll]/1/g' | \
      sed -r 's/[Oo]/0/g' | \
      sed -r 's/[Ss]/5/g' | \
      sed -r 's/[Tt]/7/g' | \
      sed -r 's/[Gg]/9/g'
  fi
done

