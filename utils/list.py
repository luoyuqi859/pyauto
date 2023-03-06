#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: list
@Created: 2023/2/25
"""


class List(list):
    def remove(self, *args):
        for arg in args:
            if arg in self:
                super().remove(arg)
        return self

    def prepend(self, *args, dup=True):
        """在列表头部添加元素"""
        for arg in args:
            if arg in self and not dup:
                self.remove(arg)
                self.insert(0, arg)
                return self
            self.insert(0, arg)
        return self

    def append(self, *args, dup=True):
        for arg in args:
            if arg in self and not dup:
                continue
            super().append(arg)
        return self

    def extend(self, *args, dup=True):
        return self.append(*args, dup=dup)

    def diff(self, other):
        """
        对比两个list之间的不同
        :param other: （missing_set, extra_set）
        :return:
        """
        missing, extra = set(), set()

        def _diff(this, another):
            if not this:
                missing.union(another)
            elif not another:
                extra.union(this)
            else:
                this_pop = this.pop(0)
                another_pop = another.pop(0)
                if this_pop != another_pop:
                    if this_pop not in other and another_pop in self:
                        extra.add(this_pop)
                        another.insert(0, another_pop)
                    elif another_pop not in self and this_pop in other:
                        missing.add(another_pop)
                        this.insert(0, this_pop)
                    elif this_pop not in other and another_pop not in self:
                        extra.add(this_pop)
                        missing.add(another_pop)
                _diff(this, another)

        _diff(self, other)
        return missing, extra
