#include <iostream>
#include "maze.hpp"

bool DFS(Maze<int>& maze, const point& current, const point& end, vector<string>& path) {
    if (current == end)
        return true;
    else {
        maze[current] = 0;
        for (auto n: maze.get_neighbors(current)) {
            string dir_name = n.first;
            point neighbor = n.second;
            path.emplace_back(dir_name);
            if (DFS(maze, neighbor, end, path))
                return true;
            else
                path.pop_back();
        }
        return false;
    }
}

vector<string> find_maze_path(Maze<int>& maze) {
    point start, end;
    tie(start, end) = maze.get_start_end();
    vector<string> path;
    DFS(maze, start, end, path);
    return path;
}

int main() {
    size_t n;
    cin >> n;
    Maze<int> maze(n);
    cin >> maze;
    for (const string& dir: find_maze_path(maze))
        cout << dir << endl;
    return 0;
}