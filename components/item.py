class Item:
    # A component that enables it's owner to be picked up as an item.
    # if an Entity has this component, we can pick it up, and if not, we can't.
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs