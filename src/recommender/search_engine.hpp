#pragma once

#include <string>
#include <vector>

struct Paper {
    std::string id;
    std::string title;
    std::string categories;
    std::string update_date;
    std::string autohors;
    std::vector<float> embedding;
};
struct Result {
    float score;
    Paper paper;
};
struct SearchEngine {
    SearchEngine(
        const std::string& vectors_path,
        const std::string& index_path
    );
    std::vector<Result> search(const std::vector<float>& query_vec, int k) const;
private:
    std::vector<Paper> papers_;
};