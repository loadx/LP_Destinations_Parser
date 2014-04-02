class ListItem(object):
    """
    Container class
    Represents a linked item on the DoubleLinkedList
    """
    def __init__(self, current, prev=None):
        self.index = current[0]
        self.current = current[1]
        self.prev_item = prev
        self.next_item = {}

    def __repr__(self):
        return "current: (%s, %s),  prev: %s,  next: %s" % (
            self.current, self.index,
            getattr(self.prev_item, 'current', None),
            getattr(self.next_item, 'current', None)
        )

    def __str__(self):
        return self.current


class DoubleLinkedList(object):
    """
    Helper class to maintain a double linked list
    """
    def __init__(self):
        self.tail = None
        self.head = None
        self.tree = {}

    def __getitem__(self, location_id):
        """
        Allow access as ddlist[<location_id>]
        """
        return self.tree[location_id]

    def add(self, location_id,  location_name):
        """
        Add a node to the linked list

        :param: location_id (string) - destinations geo_id
        :param: location_name (string) - name of the location
        """
        if self.head:
            self.tail = self.head

        self.head = self.tree[location_id] = ListItem((location_id, location_name), self.tail)

        if len(self.tree) > 0:
            self.set_next_pointer()
            self.set_prev_pointer()

    def set_next_pointer(self, item=None):
        """
        Set the previous item's next pointer to the `current` item

        :param: current (ListItem)
        """
        if self.tail:
            self.tail.next_item = item or self.head
            return self.tail.next_item
        else:
            return None

    def set_prev_pointer(self, item=None):
        """
        Set the previous item's rewind pointer to `tail`

        :params: tail (ListItem)
        """
        if self.tail:
            self.head.prev_item = item or self.tail
            return self.head.prev_item
        else:
            return None

    def flatten(self, start, backward=False, stack=None, **kwargs):
        prop = 'next_item'
        if backward:
            prop = 'prev_item'

        if stack is None:
            # common python idiom. Cant initialize with empty list
            # otherwise it will append on subsequent function calls
            # from self
            current = self[start]
            stack = []
            self.max_items = kwargs.get('max_items') or len(self.tree)
        else:
            current = getattr(start, prop, None)

        if len(stack) < self.max_items and current:
            stack.append(str(current))
            self.flatten(current, backward, stack)

        return stack
