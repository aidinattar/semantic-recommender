cmake_minimum_required(VERSION 3.10)
project(semantic_search)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set the compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2 -g")

# Add the executable and source files
add_executable(semantic_search
    main.cpp
    search_engine.cpp
    utils.cpp
    # Add any additional source files here
)