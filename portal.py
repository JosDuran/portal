from flask import Flask, request
from flask import render_template, redirect, url_for, send_file, make_response
from pytube import YouTube
import os
import unidecode

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("portal.html", p1="algo especial")
   
@app.route('/webcam')
def webcam():
   return render_template("webcam.html")
   
@app.route('/youtubedl', methods = ['GET','POST'])
def formprocurl():
   """Handle the form submission"""
   if request.method == 'POST':  #this block is only entered when the form is submitted    
   	yourl = request.form['yourl']
   	print(yourl)
   	yt = YouTube(yourl)
   	#streams = yt.streams.all()
   	for v in yt.streams.all():
   		print(v)
   	stream = yt.streams.filter(progressive=True, file_extension="mp4")
   	#stream.all()   	
   	stream.order_by("resolution").desc
   	ind_stream = stream.first()
   	#videos = yt.get_videos()
   	print('_______________________')
   	for v in stream.all():
   		print(v)
   	fn = ind_stream.default_filename
   	fn2 = unicode(fn, "utf-8")
   	fn3=unidecode.unidecode(fn2)
   	fn4 = fn3.replace(" ", "_")
   	print(fn2)
   	print(fn3)
   	print(fn4)
   	fn5, ext = os.path.splitext(fn4)
   	ind_stream.download(None, fn5)
   	urlres=fn4
   	#s= url_for('/'+urlres)
   	#print(s)
   	#serve_video(urlres)
   	return render_template("subbform.html", urlres=urlres)
   return render_template("subbform.html", urlres="vacio")
   
MEDIA_PATH = '/home/pi/flaskjos'

@app.route('/upload/<vid_name>')
def serve_video(vid_name):
	print("vid_name")
	print(vid_name)
	vid_path = os.path.join(MEDIA_PATH, vid_name)
	print("____s____")
	print(vid_path)
	print(vid_name)
	resp = make_response(send_file(vid_path, 'video/mp4'))
	resp.headers['Content-Disposition'] = 'inline'
	return resp
	   
if __name__ == '__main__':
   app.run(host= '192.168.1.5', port=8874, debug=True)