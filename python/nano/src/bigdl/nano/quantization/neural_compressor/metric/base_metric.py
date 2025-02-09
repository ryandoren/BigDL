#
# Copyright 2016 The BigDL Authors.
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
#
from abc import ABC, abstractmethod


class INCMetric(ABC):
    def __init__(self):
        self.pred_list = []
        self.label_list = []

    @property
    def metric(self):
        try:
            return getattr(self, '_metric')
        except AttributeError:
            raise RuntimeError("Attribute 'metric' must be set.")

    @metric.setter
    def metric(self, framework_metric):
        setattr(self, '_metric', framework_metric)

    def update(self, preds, labels):
        # add preds and labels to storage
        self.pred_list.extend(preds)
        self.label_list.extend(labels)

    def reset(self):
        # clear preds and labels storage
        self.pred_list = []
        self.label_list = []

    def result(self):
        # calculate accuracy
        preds, labels = self.stack(self.pred_list, self.label_list)
        accuracy = self.metric(preds, labels)
        return self.to_scalar(accuracy)

    @abstractmethod
    def stack(self, preds, labels):
        pass

    @abstractmethod
    def to_scalar(self, tensor):
        pass
