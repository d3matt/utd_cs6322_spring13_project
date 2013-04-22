class SortedList(object):
    def __init__(self, max_length=10):
        self.max_length=max_length
        self.list_ = []

    def insert(self, obj, value):
        self.list_.append( (obj,value) )
        self.list_.sort( key=lambda (x,y): y, reverse=True)
        if len(self.list_) > self.max_length:
            self.list_.pop()

    def __iter__(self):
        return iter(self.list_)
    def __str__(self):
        return str(self.list_)
    def __unicode__(self):
        return unicode(self.list_)

def unit_test():
    sl = SortedList(max_length=3)
    sl.insert('a', 1)
    sl.insert('b', 6)
    sl.insert('c', 4)
    print sl
    sl.insert('d', 8)
    print sl

if __name__ == "__main__":
    unit_test()
