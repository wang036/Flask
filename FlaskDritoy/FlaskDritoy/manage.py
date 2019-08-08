"""
项目管理文件
"""

from FlaskDritoy.models import models
from FlaskDritoy.views import app

if __name__ == "__main__":
    models.create_all()
    app.run(debug=True, port=8000)
