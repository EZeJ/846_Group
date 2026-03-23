class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy_add = [0] * (4 * n)
        self.lazy_set = [None] * (4 * n)

    def _apply(self, node, start, end, add_value=0, set_value=None):
        if set_value is not None:
            self.tree[node] = (end - start + 1) * set_value
            self.lazy_set[node] = set_value
            self.lazy_add[node] = 0
        if add_value != 0:
            self.tree[node] += (end - start + 1) * add_value
            if self.lazy_set[node] is not None:
                self.lazy_set[node] += add_value
            else:
                self.lazy_add[node] += add_value

    def _push(self, node, start, end):
        mid = (start + end) // 2
        left = 2 * node + 1
        right = 2 * node + 2

        if self.lazy_set[node] is not None:
            self._apply(left, start, mid, set_value=self.lazy_set[node])
            self._apply(right, mid + 1, end, set_value=self.lazy_set[node])
            self.lazy_set[node] = None

        if self.lazy_add[node] != 0:
            self._apply(left, start, mid, add_value=self.lazy_add[node])
            self._apply(right, mid + 1, end, add_value=self.lazy_add[node])
            self.lazy_add[node] = 0

    def _update_range(self, node, start, end, l, r, add_value=0, set_value=None):
        if start > r or end < l:
            return

        if l <= start and end <= r:
            self._apply(node, start, end, add_value, set_value)
            return

        self._push(node, start, end)
        mid = (start + end) // 2
        left = 2 * node + 1
        right = 2 * node + 2
        self._update_range(left, start, mid, l, r, add_value, set_value)
        self._update_range(right, mid + 1, end, l, r, add_value, set_value)
        self.tree[node] = self.tree[left] + self.tree[right]

    def _query_range(self, node, start, end, l, r):
        if start > r or end < l:
            return 0

        if l <= start and end <= r:
            return self.tree[node]

        self._push(node, start, end)
        mid = (start + end) // 2
        left = 2 * node + 1
        right = 2 * node + 2
        return self._query_range(left, start, mid, l, r) + self._query_range(right, mid + 1, end, l, r)

    def add_range(self, l, r, value):
        self._update_range(0, 0, self.n - 1, l, r, add_value=value)

    def set_range(self, l, r, value):
        self._update_range(0, 0, self.n - 1, l, r, set_value=value)

    def range_sum(self, l, r):
        return self._query_range(0, 0, self.n - 1, l, r)


def process_queries(nums, operations):
    n = len(nums)
    seg_tree = SegmentTree(n)

    # Initialize the segment tree with the initial array values
    for i, num in enumerate(nums):
        seg_tree.add_range(i, i, num)

    results = []

    for op in operations:
        if op[0] == "add":
            _, l, r, x = op
            seg_tree.add_range(l, r, x)
        elif op[0] == "set":
            _, l, r, x = op
            seg_tree.set_range(l, r, x)
        elif op[0] == "sum":
            _, l, r = op
            results.append(seg_tree.range_sum(l, r))

    return results