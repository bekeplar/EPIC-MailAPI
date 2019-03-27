class Group:
    """class to contain all group objects"""

    def __init__(self, **kwargs):
        self.group_id = kwargs["group_id"]
        self.group_name = kwargs["group_name"]
        self.is_admin = True