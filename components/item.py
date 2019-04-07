class Item:
    # A component that enables it's owner to be picked up as an item.
    # if an Entity has this component, we can pick it up, and if not, we can't.
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs