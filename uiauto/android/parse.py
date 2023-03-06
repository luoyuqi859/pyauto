#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: parse
@Created: 2023/2/25
"""
import re
from xml.sax.handler import ContentHandler

from lxml import etree
from xml.sax import parseString


class Bounds:
    """
    限制范围
    """

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @property
    def center(self):
        """
        中心坐标

        :return:
        """
        x = (self.right + self.left) // 2
        y = (self.bottom + self.top) // 2
        return x, y

    def unpack(self):
        return self.left, self.top, self.right, self.bottom

    @staticmethod
    def parse(bounds_str):
        match = re.fullmatch(r'^\[(\d+),(\d+)\]\[(\d+),(\d+)\]$', bounds_str)
        left, top, right, bottom = match.groups()
        return Bounds(int(left), int(top), int(right), int(bottom))

    def __contains__(self, item):
        assert isinstance(item, tuple)
        return self.left <= item[0] <= self.right and self.top <= item[1] <= self.bottom


class _Node(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent = None
        self.children = []
        self.index = 1

    def __getattr__(self, item):
        return self.get(item)

    @property
    def bounds(self):
        """
        元素矩形框

        :return: tuple, (left, top, right, bottom)
        """
        bounds = self.get('bounds')
        if bounds:
            return Bounds.parse(bounds).unpack()

    @property
    def size(self):
        left, top, right, bottom = self.bounds
        return (right - left) * (bottom - top)

    def add_child(self, child):
        child.parent = self
        if not self.children:
            child.index = 1
        else:
            for c in reversed(self.children):
                if c['class'] == child['class']:
                    child.index = c.index + 1
                    break
            else:
                child.index = 1
        self.children.append(child)

    @property
    def hierarchy(self):
        output = []

        def recurse(p):
            output.append(f'<{p.tag}>')
            for child in p.children:
                recurse(child)
            output.append(f'</{p.tag}>')

        recurse(self)
        return ''.join(output)


class AndroidPageParser(object):
    """

    """

    def __init__(self, pagesource):
        self.pagesource = pagesource
        self.__target = None

    @property
    def etree(self):
        # xml 不能包含encoding='utf-8'，lxml不支持
        return etree.fromstring(re.sub(r"(encoding='.+')", '', self.pagesource))

    def find_node(self, x, y) -> _Node:
        """

        :param x:
        :param y:
        :return:
        """

        def handle(node):
            if not node.bounds:
                return False
            left, top, right, bottom = node.bounds
            if left <= x <= right and top <= y <= bottom:
                if not self.__target or self.__target.size >= node.size:
                    self.__target = node

        handler = Handler(handle)
        parseString(self.pagesource, handler)
        return self.__target

    def sub(self, xpath):
        """获取xpath指向的节点内容"""
        nodes = self.etree.xpath(xpath)
        if nodes:
            return etree.tostring(nodes[0], method='html')

    def one(self, xpath):
        """查找满足的第一个节点"""
        nodes = self.etree.xpath(xpath)
        if nodes:
            return _Node(**nodes[0].attrib)

    def all(self, xpath):
        """查找所有满足条件的节点"""
        return [_Node(**item.attrib) for item in self.etree.xpath(xpath)]


class Handler(ContentHandler):
    """
    爬虫Handler，用于解析页面
    """

    def __init__(self, handle):
        super().__init__()
        self._stack = []
        self.handle = handle

    def startElement(self, name, attrs):
        node = _Node()
        for attr, value in attrs.items():
            node[attr] = value
        if self._stack:
            self._stack[-1].add_child(node)
        self._stack.append(node)
        if self.handle:
            self.handle(node)

    def endElement(self, name):
        if self._stack:
            self._stack.pop()
