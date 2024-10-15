#!/bin/sh
set -v
docker pull bash  # For bash
docker pull gcc  # For gcc & g++
docker pull openjdk  # For javac and java
docker pull python:3  # For python3

