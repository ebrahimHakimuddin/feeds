#!/bin/bash

cd ~/feeds/
./tinyfeed -i ./inputs.txt -o ./index.html

if [[ $? -eq 0 ]]; then
    sed -i "/<footer>/a \<p>Feed Updated on $(date)</p>" index.html
    git add .
    git commit -m "Updated Feed On $(date)"
    git push
    echo "Succesfully Updated Feeds on $(date)" >> update.log
else
    echo "Could not update feed on $($?)" >> update.log 
fi
