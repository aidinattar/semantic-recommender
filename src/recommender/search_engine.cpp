#include <fstream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include "search_engine.hpp"
#include "utils.hpp"

SearchEngine::SearchEngine(
    const std::string& vectors_path,
    const std::string&   index_path
) {
    std::ifstream vfile(vectors_path);
    std::ifstream ifile(index_path);

    std::string vline, iline;
    getline(ifile, iline); // skip header
    while (getline(vfile, vline) && getline(ifile, iline)) {
        std::stringstream vss(vline);
        std::stringstream iss(iline);
        std::string val, id, title, cat;
        std::vector<float> vec;

        while (getline(vss, val, ',')) {
            vec.push_back(std::stof(val));
        }

        getline(iss, id, ',');
        getline(iss, title, ',');

        papers_.push_back({id, title, vec});
    }
}

std::vector<Result> SearchEngine::search(const std::vector<float>& query_vec, int k) const {
    std::vector<Result> scored;
    for (const auto& paper : papers_) {
        float score = cosine_similarity(query_vec, paper.embedding);
        scored.push_back({score, paper});
    }
    std::sort(scored.begin(), scored.end(), [](auto& a, auto& b) {
        return a.score > b.score;
    });
    if ((int)scored.size() > k) {
        scored.resize(k);
    }
    return scored;
}
