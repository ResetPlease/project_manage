#!/bin/bash

for file in *.sql; do
    psql -h localhost -p 5432 -U iveseen -d kp -f ./$file
    if [ $? -ne 0 ]; then
        echo "Error processing $file"
        break
    else
        echo "done"
    fi
done
