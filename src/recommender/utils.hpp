#pragma once

#include <vector>
#include <string>

float cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2);
std::vector<float> parse_vector(const std::string& vec_str);
std::vector<std::vector<float>> load_vectors_bin(const std::string& filename, size_t num_vectors, size_t dim);