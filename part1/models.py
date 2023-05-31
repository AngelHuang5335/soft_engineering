from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50)
    car_id = models.IntegerField(null=True)
    car_capacity = models.IntegerField(null=True)
    is_admin = models.IntegerField()
    token = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username

    class Meta:
        # 定义数据表名
        db_table = 'User'
        # 表别名
        verbose_name = '用户'
        # 表别名复数，用于英文显示
        verbose_name_plural = verbose_name


class User_list:
    online_list = []

    def user_online(self, user):
        self.online_list.append(user)
        print(len(self.online_list))
        self.print_online_user()

    def user_offline(self, token):
        user = User.objects.get(token=token)
        self.online_list.remove(user)
        print(len(self.online_list))
        self.print_online_user()

    def judge_user_online(self, token):
        if User.objects.filter(token=token).exists():
            if User.objects.get(token=token) in self.online_list:
                return 1
            else:
                return 0
        else:
            return 0

    def check_user_online(self, user):
        if user in self.online_list:
            return 1
        else:
            return 0

    def judge_user_token(self, token):
        if self.judge_user_online(token):
            return 0, 0    # 用户未登录
        else:
            user = User.objects.get(token=token)
            if user.is_admin == 0:
                return 1, user.car_id    # 普通用户
            else:
                return 0, 0

    def judge_admin_token(self, token):
        if self.judge_user_online(token):
            return 0    # 用户未登录
        else:
            user = User.objects.get(token=token)
            if user.is_admin == 1:
                return 1    # 管理员
            else:
                return 0

    def print_online_user(self):
        for i in self.online_list:
            print('online username:', i.username)
