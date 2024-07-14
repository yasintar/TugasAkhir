#!/bin/sh
cd image/
ls -F *.jpg | head -n -1 | xargs -r rm
cd ..
