#ifndef QBSEARCH_INPUT_H
#define QBSEARCH_INPUT_H

#include "ttnn/operations/atanh.hpp"
#include "ttnn/operations/asinh.hpp"

// --- BEGIN AUTO‑GENERATED BLUEPRINT -------------------------------------------------
// Optimized implementation for atanh/asinh using the identity:
//   atanh(x) = 0.5 * log((1 + x) / (1 - x))
//   asinh(x) = log(x + sqrt(x*x + 1))
// This replaces the previous element‑wise loops with a single fused kernel.
// -------------------------------------------------------------------------------

inline ttnn::Tensor atanh_optimized(const ttnn::Tensor& input) {
    // Fuse the computation into a single kernel call.
    // NOTE: The underlying kernel expects the input to be in the range (-1, 1).
    return ttnn::operations::atanh::atanh_fused(input);
}

inline ttnn::Tensor asinh_optimized(const ttnn::Tensor& input) {
    // Fuse the computation into a single kernel call.
    return ttnn::operations::asinh::asinh_fused(input);
}

// Public API Redirection
inline ttnn::Tensor atanh(const ttnn::Tensor& input) {
    return atanh_optimized(input);
}

inline ttnn::Tensor asinh(const ttnn::Tensor& input) {
    return asinh_optimized(input);
}

// --- END AUTO‑GENERATED BLUEPRINT ---------------------------------------------------

#endif // QBSEARCH_INPUT_H