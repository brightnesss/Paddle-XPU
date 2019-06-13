// Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "paddle/fluid/lite/core/mir/conv_elementwise_add_relu_fuse_pass.h"
#include <memory>
#include <vector>
#include "paddle/fluid/lite/core/mir/fusion/conv_elementwise_add_relu_fuser.h"
#include "paddle/fluid/lite/core/mir/pass_registry.h"

namespace paddle {
namespace lite {
namespace mir {

void ConvElementwiseAddReLUFusePass::Apply(
    const std::unique_ptr<SSAGraph>& graph) {
  fusion::ConvElementwiseAddReLUFuser fuser;
  fuser(graph.get());
}

}  // namespace mir
}  // namespace lite
}  // namespace paddle

REGISTER_MIR_PASS(lite_conv_elementwise_add_act_fuse_pass,
                  paddle::lite::mir::ConvElementwiseAddReLUFusePass);
