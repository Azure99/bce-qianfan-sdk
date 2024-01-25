# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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
"""
data source including file
"""

from qianfan.dataset.data_source.base_data_source import DataSource
from qianfan.dataset.data_source.bos_data_source import BosDataSource
from qianfan.dataset.data_source.data_source_utils import FormatType
from qianfan.dataset.data_source.file_data_source import FileDataSource
from qianfan.dataset.data_source.qianfan_data_source import QianfanDataSource

__all__ = [
    "DataSource",
    "FileDataSource",
    "QianfanDataSource",
    "BosDataSource",
    "FormatType",
]