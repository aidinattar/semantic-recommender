#include <fstream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include "search_engine.hpp"
#include "utils.hpp"


SearchEngine::SearchEngine(
    const std::string& vectors_path,
    const std::string& index_path
) {
    // 1. Read metadata from index file
    std::ifstream ifile(index_path);
    if (!ifile) throw std::runtime_error("Cannot open index file: " + index_path);

    std::string iline;
    std::getline(ifile, iline); // skip header

    const char SEP = '\x1f';
    std::vector<std::string> ids, titles, cats, update_dates, authors;

    while (std::getline(ifile, iline)) {
        std::stringstream iss(iline);
        std::string id, title, cat, update_date, author;

        std::getline(iss, id, SEP);
        std::getline(iss, title, SEP);
        std::getline(iss, cat, SEP);
        std::getline(iss, update_date, SEP);
        std::getline(iss, author, SEP);

        ids.push_back(id);
        titles.push_back(title);
        cats.push_back(cat);
        update_dates.push_back(update_date);
        authors.push_back(author);
    }

    size_t num_vectors = ids.size();
    size_t dim = 384;

    // 2. Read vectors from binary file
    std::ifstream vfile(vectors_path, std::ios::binary);
    if (!vfile) throw std::runtime_error("Cannot open vectors file: " + vectors_path);

    for (size_t i = 0; i < num_vectors; ++i) {
        std::vector<float> vec(dim);
        vfile.read(reinterpret_cast<char*>(vec.data()), dim * sizeof(float));

        if (!vfile) {
            throw std::runtime_error("Error reading vector data from file: " + vectors_path);
        }

        papers_.push_back({ids[i], titles[i], cats[i], update_dates[i], authors[i], vec});
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