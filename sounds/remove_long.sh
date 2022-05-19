#!/bin/bash

for i in "long"*; do mv "$i" "${i#"long"}"; done
