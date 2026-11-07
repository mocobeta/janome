# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class ProgressHandler(ABC):
    """
    Base progress handler class
    """

    @abstractmethod
    def on_start(self, total: int, value: float = 0, desc: Optional[str] = None):
        pass

    @abstractmethod
    def on_progress(self, value: float = 1):
        pass

    @abstractmethod
    def on_complete(self):
        pass


class SimpleProgressIndicator(ProgressHandler):
    def __init__(self, update_frequency: float = 0.0001, format: Optional[str] = None):
        self.update_frequency = update_frequency
        self.format = format or "\r{}: {:.1f}% | {}/{}"
        self.total: Optional[int] = None
        self.value: Optional[float] = None
        self.desc: Optional[str] = None

    def print_progress(self, terminator: str = ""):
        if self.total is None or self.value is None:
            return
        handler.terminator = terminator
        logger.info(self.format.format(self.desc, self.value * 100 / self.total, self.value, self.total))

    def on_start(self, total: int, value: float = 0, desc: Optional[str] = None):
        self.total = total
        self.value = value
        self.desc = desc or "Processing"

    def on_progress(self, value: float = 1):
        if self.value is None:
            raise RuntimeError("Progress has not started")
        self.value += value

        if float(self.value * self.update_frequency).is_integer():
            self.print_progress()

    def on_complete(self):
        self.print_progress("\n")
        self.total = self.value = self.desc = None
