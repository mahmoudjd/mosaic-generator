class Counter:
    def __init__(self, total):
        """
        The function __init__() is a special function that is automatically called whenever a new
        instance of the class is created
        @param total - The total number of items to be processed.
        """
        self.total = total
        self.counter = 0

    def increment(self):
        """
        It takes a counter and a total, and prints a percentage of the counter to the total
        """
        self.counter += 1
        actual_value = (self.counter * 100) / self.total
        print('[...] processing: {:02.0f}%'.format(actual_value), flush=True, end='\r')
        
