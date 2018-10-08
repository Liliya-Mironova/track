class Item:
    def __init__(self, data, prev_item=None, next_item=None):
        self.data = data
        self.prev_item = prev_item
        self.next_item = next_item


class DoubleLinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.count = 0

    def push(self, data):
        if self.count == 0:
            self.first = Item(data)
            self.last = self.first
        elif self.count > 0:
            self.last.next_item = Item(data, self.last, None)
            self.last = self.last.next_item
        self.count += 1

    def pop(self):
        if self.count == 0:
            raise RuntimeError("Cannot pop from an empty list")
        result = self.last.data
        if self.count == 1:
            self.first = None
            self.last = None
        else:
            self.last = self.last.prev_item
            self.last.next_item = None
        self.count -= 1
        return result

    def shift(self, data):
        if self.count == 0:
            self.first = Item(data)
            self.last = self.first
        elif self.count > 0:
            self.first.prev_item = Item(data, None, self.first)
            self.first = self.first.prev_item
        self.count += 1

    def unshift(self):
        if self.count == 0:
            raise RuntimeError("Cannot pop from an empty list")
        result = self.first.data
        if self.count == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next_item
            self.first.prev_item = None
        self.count -= 1
        return result

    def contains(self, data):
        if self.count == 0:
            return False
        if self.count > 0:
            cursor = self.first
            for i in range(self.count):
                if cursor.data == data:
                    return True
                cursor = cursor.next_item
        return False

    def delete(self, data):
        if self.count == 0:
            raise RuntimeError("Cannot delete from an empty list")

        cursor = self.first
        for i in range(self.count):
            if cursor.data == data:
                if cursor == self.first:
                    self.first = cursor.next_item
                elif cursor == self.last:
                    self.last = cursor.prev_item
                else:
                    cursor.prev_item.next_item = cursor.next_item
                    cursor.next_item.prev_item = cursor.prev_item
                cursor.prev_item = None
                cursor.next_item = None
                cursor.data = None
                self.count -= 1
                return
            cursor = cursor.next_item
        raise RuntimeError("There is no such element to delete")

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last

    def len(self):
        return self.count

    def __repr__(self):
        if self.count == 0:
            raise RuntimeError("Try to print an empty list")
        cursor = self.first
        result = ""
        for i in range(self.count):
            result += "{}".format(cursor.data)
            cursor = cursor.next_item
            if cursor is not None:
                result += " <-> "
        return result


# dll = DoubleLinkedList()
# dll.push(1)
# dll.shift(2)
# dll.push(3)
# dll.push(4)
# dll.shift(5)

# print(dll.contains(1))
# dll.delete(2)
# print(dll.contains(2))
# print(dll)
