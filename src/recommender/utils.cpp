#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <fstream>
#include <sstream>
#include "utils.hpp"

#include <iostream>

float cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2) {
    // std::cout << vec1.size() << " " << vec2.size() << std::endl;
    if (vec1.size() != vec2.size()) {
        throw std::invalid_argument("Vectors must be of the same size");
    }
    float dot_product = 0.0f;
    float norm_a = 0.0f;
    float norm_b = 0.0f;
    for (size_t i = 0; i < vec1.size(); ++i) {
        dot_product += vec1[i] * vec2[i];
        norm_a += vec1[i] * vec1[i];
        norm_b += vec2[i] * vec2[i];
    }
    return dot_product / (std::sqrt(norm_a) * std::sqrt(norm_b));
}

std::vector<float> parse_vector(const std::string& vec_str) {
    std::vector<float> result;
    std::string token;
    std::stringstream ss(vec_str);

    std::ofstream log("log.txt", std::ios_base::app);

    while (std::getline(ss, token, ',')) {
        try {
            result.push_back(std::stof(token));
        } catch (const std::invalid_argument&) {
            log << "Warning: Invalid value '" << token << "' in vector: " << vec_str << "\n";
            result.push_back(0.0f); // fallback
        } catch (const std::out_of_range&) {
            log << "Warning: value '" << token << "' out of range in vector string: " << vec_str << "\n";
            result.push_back(0.0f); // fallback
        }
    }

    return result;
}