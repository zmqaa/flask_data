from flask_login import LoginManager

login_manager = LoginManager()

# 用户加载：当用户通过登录成功后，Flask-Login 会将用户的 ID 存储在会话中。
# 在后续请求中，Flask-Login 会根据这个 ID 来恢复用户的状态。
#
# 查询用户：load_user(user_id) 函数会接收一个用户 ID，并通过查询数据库来获取对应的用户对象。
# 在这个例子中，User.query.get(int(user_id)) 会返回与给定 ID 匹配的用户实例。
#
# 身份验证：如果用户存在，Flask-Login 会将该用户对象存储在当前会话中，方便后续的身份验证和权限检查。
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

