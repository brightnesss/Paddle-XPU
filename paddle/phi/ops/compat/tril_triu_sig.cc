/* Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

#include "paddle/phi/core/compat/op_utils.h"

namespace phi {

KernelSignature TrilTriuOpArgumentMapping(const ArgumentMappingContext& ctx) {
  return KernelSignature("tril", {"X"}, {"diagonal", "lower"}, {"Out"});
}

KernelSignature TrilTriuGradOpArgumentMapping(
    const ArgumentMappingContext& ctx) {
  return KernelSignature(
      "tril_grad", {"Out@GRAD"}, {"diagonal", "lower"}, {"X@GRAD"});
}

}  // namespace phi

PD_REGISTER_BASE_KERNEL_NAME(tril_triu, tril);
PD_REGISTER_BASE_KERNEL_NAME(tril_triu_grad, tril_grad);

PD_REGISTER_ARG_MAPPING_FN(tril_triu, phi::TrilTriuOpArgumentMapping);
PD_REGISTER_ARG_MAPPING_FN(tril_triu_grad, phi::TrilTriuGradOpArgumentMapping);
