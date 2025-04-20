#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "search_engine.hpp"
#include "utils.hpp"

std::vector<float> load_query_vector(const std::string& path) {
    std::ifstream file(path);
    std::string line;
    std::vector<float> vec;
    if (getline(file, line)) {
        std::stringstream ss(line);
        std::string val;
        while (getline(ss, val, ',')) {
            vec.push_back(std::stof(val));
        }
    }
    return vec;
}

int main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " query.csv vectors.csv index.csv k" << std::endl;
        return 1;
    }

    std::string query_path = argv[1];
    std::string vectors_path = argv[2];
    std::string index_path = argv[3];
    int k = std::stoi(argv[4]);

    auto query_vec = load_query_vector(query_path);
    SearchEngine engine(vectors_path, index_path);
    auto results = engine.search(query_vec, k);

    std::cout << "\nTop " << k << " results:\n";
    for (size_t i = 0; i < results.size(); ++i) {
        const auto& r = results[i];
        std::cout << i + 1 << ". [" << r.paper.id << "] " << r.paper.title
                  << " (score: " << r.score << ")\n";
    }

    return 0;
}
