cmake_minimum_required(VERSION 3.12)
project(tsp)

set(CMAKE_CXX_STANDARD 14)

add_executable(tsp main.cpp)
add_executable(input random.cpp)