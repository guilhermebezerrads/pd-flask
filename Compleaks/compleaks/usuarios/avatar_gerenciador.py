import os
from PIL import Image
from flask import url_for, current_app

def adicionar_avatar(upload_avatar, username):

	filename = upload_avatar.filename

	ext_type = filename.split('.')[-1]

	storage_filename = str(username)+'.'+ext_type

	filepath = os.path.join(current_app.root_path, 'static/imagens/avatares', storage_filename)

	tamanho = (300,300)

	pic = Image.open(upload_avatar)
	pic.thumbnail(tamanho)
	pic.save(filepath)

	return storage_filename