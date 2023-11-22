class MinHeapNode:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, new_priority, new_value):
        node = MinHeapNode(new_priority, new_value)
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def is_empty(self):
        return len(self.heap) == 0

    def _heapify_up(self, child_index):
        while child_index > 0:
            parent_index = (child_index - 1) // 2
            if self._compare_nodes(child_index, parent_index):
                self._swap_nodes(child_index, parent_index)
                child_index = parent_index
            else:
                break

    def _heapify_down(self, parent_index):
        left_child_index = 2 * parent_index + 1
        right_child_index = 2 * parent_index + 2
        smallest = parent_index

        if left_child_index < len(self.heap) and self._compare_nodes(left_child_index, smallest):
            smallest = left_child_index

        if right_child_index < len(self.heap) and self._compare_nodes(right_child_index, smallest):
            smallest = right_child_index

        if smallest != parent_index:
            self._swap_nodes(parent_index, smallest)
            self._heapify_down(smallest)

    def get_heap_elements(self):
        return [node.value for node in self.heap]

    def _compare_nodes(self, index1, index2):
        return self.heap[index1].priority < self.heap[index2].priority

    def _swap_nodes(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
