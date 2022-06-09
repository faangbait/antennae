#!/bin/bash
# TODO: Optimize search depth
# TODO: Cronjob this

CHESS_STORAGE="/mnt/bulk/chess"

for PGN_SOURCE in ${CHESS_STORAGE}/imported/*; do
    echo "Found ready file ${PGN_SOURCE}"

    ./pgn-extract -7CNV -Wuci --fixtagstrings --fixresulttags --detag Annotator "${PGN_SOURCE}" | \
    nice -n 10 ./uci-analyze --engine ./stockfish --bookdepth 4 --searchdepth 40 --annotatePGN --setoption "SyzygyPath" "/mnt/bulk/tablebases/3-4-5:/mnt/bulk/tablebases/6-DTZ:/mnt/bulk/tablebases/6-WDL:/mnt/bulk/tablebases/7-DTZ:/mnt/bulk/tablebases/7-WDL" --setoption "Threads" 10 --setoption "Hash" 2048 --setoption "Move Overhead" 0 | \
    ./pgn-extract -eeco.pgn --output "${CHESS_STORAGE}/annotated/$(basename ${PGN_SOURCE})"
    
    rm "${PGN_SOURCE}"

done

