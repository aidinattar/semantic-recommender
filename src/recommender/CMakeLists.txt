cmake_minimum_required(VERSION 3.10)
project(semantic_search)

# Imposta lo standard C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Abilita simboli di debug e warning
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2 -g")

# Aggiungi l'eseguibile e i file sorgente
add_executable(semantic_search
    main.cpp
    search_engine.cpp
    utils.cpp
)
