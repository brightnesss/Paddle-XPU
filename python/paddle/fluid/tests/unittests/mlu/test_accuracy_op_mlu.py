#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import numpy as np
import sys

sys.path.append('..')
from op_test import OpTest
import paddle
import paddle.fluid as fluid
from paddle.fluid import compiler, Program, program_guard

paddle.enable_static()


class TestAccuracyOp(OpTest):
    def setUp(self):
        self.op_type = "accuracy"
        self.place = paddle.device.MLUPlace(0)
        self.__class__.use_mlu = True
        self.dtype = np.float32
        self.init_dtype()
        n = 8192
        infer = np.random.random((n, 1)).astype(self.dtype)
        indices = np.random.randint(0, 2, (n, 1)).astype('int32')
        label = np.random.randint(0, 2, (n, 1)).astype('int32')
        self.inputs = {'Out': infer, 'Indices': indices, "Label": label}
        num_correct = 0
        for rowid in range(n):
            for ele in indices[rowid]:
                if ele == label[rowid]:
                    num_correct += 1
                    break
        self.outputs = {
            'Accuracy': np.array([num_correct / float(n)]).astype(self.dtype),
            'Correct': np.array([num_correct]).astype("int32"),
            'Total': np.array([n]).astype("int32"),
        }

    def init_dtype(self):
        pass

    def test_check_output(self):
        self.check_output_with_place(self.place)


class TestAccuracyOpFp16(TestAccuracyOp):
    def init_dtype(self):
        self.dtype = np.float16

    def test_check_output(self):
        self.check_output_with_place(self.place, atol=1e-3)


class TestAccuracyOpError(unittest.TestCase):
    def test_errors(self):
        with program_guard(Program(), Program()):
            # The input type of accuracy_op must be Variable.
            x1 = fluid.create_lod_tensor(
                np.array([[-1]]), [[1]], fluid.MLUPlace(0)
            )
            label = fluid.layers.data(
                name='label', shape=[-1, 1], dtype="int32"
            )
            self.assertRaises(TypeError, fluid.layers.accuracy, x1, label)
            self.assertRaises(TypeError, paddle.metric.accuracy, x1, label)
            # The input dtype of accuracy_op must be float32 or float64.
            x2 = fluid.layers.data(name='x2', shape=[4], dtype="int32")
            self.assertRaises(TypeError, fluid.layers.accuracy, x2, label)
            self.assertRaises(TypeError, paddle.metric.accuracy, x2, label)
            x3 = fluid.layers.data(name='input', shape=[-1, 2], dtype="float16")
            fluid.layers.accuracy(input=x3, label=label)
            paddle.metric.accuracy(input=x3, label=label)


class TestAccuracyAPI1(unittest.TestCase):
    def setUp(self):
        self.predictions = paddle.static.data(
            shape=[2, 5], name="predictions", dtype="float32"
        )
        self.label = paddle.static.data(
            shape=[2, 1], name="labels", dtype="int32"
        )
        self.result = paddle.static.accuracy(
            input=self.predictions, label=self.label, k=1
        )
        self.input_predictions = np.array(
            [[0.2, 0.1, 0.4, 0.1, 0.1], [0.2, 0.3, 0.1, 0.15, 0.25]],
            dtype="float32",
        )
        self.input_labels = np.array([[2], [0]], dtype="int32")
        self.expect_value = np.array([0.5], dtype='float32')

    def test_api(self):
        exe = paddle.static.Executor()
        (result,) = exe.run(
            feed={
                "predictions": self.input_predictions,
                'labels': self.input_labels,
            },
            fetch_list=[self.result.name],
        )
        self.assertEqual((result == self.expect_value).all(), True)


class TestAccuracyAPI2(unittest.TestCase):
    def test_api(self):
        with fluid.dygraph.guard():
            predictions = paddle.to_tensor(
                [[0.2, 0.1, 0.4, 0.1, 0.1], [0.2, 0.3, 0.1, 0.15, 0.25]],
                dtype='float32',
            )
            label = paddle.to_tensor([[2], [0]], dtype="int32")
            result = paddle.static.accuracy(input=predictions, label=label, k=1)
            expect_value = np.array([0.5], dtype='float32')
            self.assertEqual((result.numpy() == expect_value).all(), True)


class TestAccuracyAPI(unittest.TestCase):
    def test_api(self):
        with fluid.dygraph.guard():
            predictions = paddle.to_tensor(
                [[0.2, 0.1, 0.4, 0.1, 0.1], [0.2, 0.3, 0.1, 0.15, 0.25]],
                dtype='float32',
            )
            label = paddle.to_tensor([[2], [0]], dtype="int32")
            result = paddle.metric.accuracy(input=predictions, label=label, k=1)
            expect_value = np.array([0.5], dtype='float32')

            self.assertEqual((result.numpy() == expect_value).all(), True)


if __name__ == '__main__':
    unittest.main()
