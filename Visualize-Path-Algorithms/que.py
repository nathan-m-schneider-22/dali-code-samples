class Node:
    def __init__(self, data):
        self.next = None
        self.prev = None
        self.data = data


class Que:
    def __init__(self):
        self.sentinel = Node(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

    def append(self,data):
        new_node = Node(data)
        self.sentinel.prev.next = new_node
        new_node.prev = self.sentinel.prev
        self.sentinel.prev = new_node
        new_node.next = self.sentinel

    def popleft(self):
        left_node = self.sentinel.next
        self.sentinel.next = left_node.next
        self.sentinel.next.prev = self.sentinel
        return left_node.data

    def is_empty(self):
        return self.sentinel.next == self.sentinel