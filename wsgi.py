from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)

# import sys
#
# path = '/home/zmqa/flask_data'  # 路径规则为 /home/你的用户名/项目文件夹名
# if path not in sys.path:
#     sys.path.append(path)
#
# from app import create_app
# application = create_app()
#
# if __name__ == '__main__':
#     application.run()