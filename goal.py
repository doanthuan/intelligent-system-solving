class Goal:
    def __init__(self, goal_type, goal_data):
        self.goal_type = goal_type
        self.goal_data = goal_data
        self.status = False # Trạng thái đã được tìm thấy hay chưa