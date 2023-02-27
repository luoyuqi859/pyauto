#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: selector
@Created: 2023/2/27 9:35
"""
from utils.dict import Dict


class Selector(dict):
    """The class is to build parameters for UiSelector passed to Android device.
    """
    __fields = {
        "text": (0x01, None),  # MASK_TEXT,
        "textContains": (0x02, None),  # MASK_TEXTCONTAINS,
        "textMatches": (0x04, None),  # MASK_TEXTMATCHES,
        "textStartsWith": (0x08, None),  # MASK_TEXTSTARTSWITH,
        "className": (0x10, None),  # MASK_CLASSNAME
        "classNameMatches": (0x20, None),  # MASK_CLASSNAMEMATCHES
        "description": (0x40, None),  # MASK_DESCRIPTION
        "descriptionContains": (0x80, None),  # MASK_DESCRIPTIONCONTAINS
        "descriptionMatches": (0x0100, None),  # MASK_DESCRIPTIONMATCHES
        "descriptionStartsWith": (0x0200, None),  # MASK_DESCRIPTIONSTARTSWITH
        "checkable": (0x0400, False),  # MASK_CHECKABLE
        "checked": (0x0800, False),  # MASK_CHECKED
        "clickable": (0x1000, False),  # MASK_CLICKABLE
        "longClickable": (0x2000, False),  # MASK_LONGCLICKABLE,
        "scrollable": (0x4000, False),  # MASK_SCROLLABLE,
        "enabled": (0x8000, False),  # MASK_ENABLED,
        "focusable": (0x010000, False),  # MASK_FOCUSABLE,
        "focused": (0x020000, False),  # MASK_FOCUSED,
        "selected": (0x040000, False),  # MASK_SELECTED,
        "packageName": (0x080000, None),  # MASK_PACKAGENAME,
        "packageNameMatches": (0x100000, None),  # MASK_PACKAGENAMEMATCHES,
        "resourceId": (0x200000, None),  # MASK_RESOURCEID,
        "resourceIdMatches": (0x400000, None),  # MASK_RESOURCEIDMATCHES,
        "index": (0x800000, 0),  # MASK_INDEX,
        "instance": (0x01000000, 0)  # MASK_INSTANCE,
    }
    __mask, __childOrSibling, __childOrSiblingSelector = "mask", "childOrSibling", "childOrSiblingSelector"

    def __init__(self, **kwargs):
        super(Selector, self).__init__(**{})
        super(Selector, self).__setitem__(self.__mask, 0)
        super(Selector, self).__setitem__(self.__childOrSibling, [])
        super(Selector, self).__setitem__(self.__childOrSiblingSelector, [])
        for k in kwargs:
            if k == 'content':
                self['description'] = kwargs[k]
            elif k == 'contentContains' or k == 'content_contains':
                self['descriptionContains'] = kwargs[k]
            elif k == 'contentMatches' or k == 'content_matches':
                self['descriptionMatches'] = kwargs[k]
            elif k == 'contentStartsWith' or k == 'content_starts_with':
                self['descriptionStartsWith'] = kwargs[k]
            elif k == 'id':
                self['resourceId'] = kwargs[k]
            elif k == 'instance':
                self['instance'] = kwargs[k] - 1
            else:
                self[k] = kwargs[k]

    def __str__(self):
        """ remove useless part for easily debugger """
        selector = self.copy()
        selector.pop('mask')
        for key in ('childOrSibling', 'childOrSiblingSelector'):
            if not selector.get(key):
                selector.pop(key)
        args = []
        for (k, v) in selector.items():
            args.append(k + '=' + repr(v))
        return 'Selector [' + ', '.join(args) + ']'

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(Selector, self).__setitem__(k, v)
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k][0])

    def __delitem__(self, k):
        if k in self.__fields:
            super(Selector, self).__delitem__(k)
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k][0])

    def clone(self):
        kwargs = dict((k, self[k]) for k in self if k not in [
            self.__mask, self.__childOrSibling, self.__childOrSiblingSelector
        ])
        selector = Selector(**kwargs)
        for v in self[self.__childOrSibling]:
            selector[self.__childOrSibling].append(v)
        for s in self[self.__childOrSiblingSelector]:
            selector[self.__childOrSiblingSelector].append(s.clone())
        return selector

    def child(self, **kwargs):
        self[self.__childOrSibling].append("child")
        self[self.__childOrSiblingSelector].append(Selector(**kwargs))
        return self

    def sibling(self, **kwargs):
        self[self.__childOrSibling].append("sibling")
        self[self.__childOrSiblingSelector].append(Selector(**kwargs))
        return self

    def update_instance(self, i):
        # update inside child instance
        if self[self.__childOrSiblingSelector]:
            self[self.__childOrSiblingSelector][-1]['instance'] = i - 1
        else:
            self['instance'] = i - 1  # ???????????????
        return self

    @staticmethod
    def parse(expr: str):
        """
        解析并将字符串表达式转换为 Selector

        :param expr:
        :return: list of Selector
        """
        selectors = []
        if '=' not in expr:
            selectors = selectors + Selector.parse('text=' + expr)
            selectors = selectors + Selector.parse('content=' + expr)
            return selectors
        expr = expr.replace('content=', 'description=')
        expr = expr.replace('content-desc=', 'description=')
        expr = expr.replace('id=', 'resourceId=')
        expr = expr.replace('class=', 'className=')
        d = Dict.from_query_str(expr)
        for k, v in d.items():
            if v[0] == v[-1] == '%':
                d.pop(k)
                d[k + 'Contains'] = v[1:-1]
            elif v[-1] == '%':
                d.pop(k)
                d[k + 'StartsWith'] = v[:-1]
            elif v[:2] == "r'" and v[-1] == "'":
                d.pop(k)
                d[k + 'Matches'] = v[2:-1]
            elif v.lower() == 'true':
                d[k] = True
            elif v.lower() == 'false':
                d[k] = False
        return [Selector(**d)]
