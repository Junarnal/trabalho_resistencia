#!/bin/bash

nome_arquivo=$1
executavel=$2

exec g++ $nome_arquivo -o $executavel -lsfml-graphics -lsfml-window -lsfml-system
