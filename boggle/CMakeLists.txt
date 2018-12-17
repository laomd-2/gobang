cmake_minimum_required(VERSION 3.13)
project(boggle)

set(CMAKE_CXX_STANDARD 17)
include_directories("include")

add_executable(boggle main.cpp board.cpp boggle_solver.cpp trie.cpp)
add_executable(test_trie test/main.cpp)