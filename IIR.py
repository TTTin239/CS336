import matplotlib.pyplot as plt
import colorsys
from math import ceil, sqrt
from PIL import Image, ImageFilter
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
from numpy import asarray, copy
from scipy.signal import convolve2d
from os import listdir
from os.path import isfile, join
import tqdm

IMFOLD = 'C:/Users/Enterprise/Downloads/test1/image.orig'

def rgbhsv(R, G, B):
	r = R/255
	g = G/255
	b = B/255
	vmax = max(r, g, b)
	vmin = min(r, g, b)
	delta = vmax - vmin
	t = -1
	if vmin == vmax:
		t = vmin
	else:
		if r == vmax:
			t = (g-b)/(vmax - vmin)
		if g == vmax:
			t = (b-r)/(vmax - vmin)
		if b == vmax:
			t = (r-g)/(vmax - vmin)
	if t >= 0:
		h = (t*60) % 360
	else:
		h = (t*60) % 360 + 360
		
	if delta==0 or vmax==0:
		s = 0
	else:
		s = delta/vmax		
	v = vmax
	return h, s, v

def hsvrgb(h, s, v):
	c = v * s
	x = c * (1- abs((h/60) %2 - 1))
	m = v - c
	if h >= 0 and h < 60:
		r = c
		g = x
		b = 0
	if h >= 60 and h < 120:
		r = x
		g = c
		b = 0
	if h >= 120 and h < 180:
		r = 0
		g = c
		b = x
	if h >= 180 and h < 240:
		r = 0
		g = x
		b = c
	if h >= 240 and h < 300:
		r = x
		g = 0
		b = c
	if h >= 300 and h < 360:
		r = c
		g = 0
		b = x
	return int((r+m) * 255), int((g+m) * 255), int((b+m) * 255)
	
def convertToHSV(im):
	for i in range(len(im)):
		for j in range(len(im[0])):
			h, s, v = rgbhsv(im[i][j][0], im[i][j][1], im[i][j][2])
			im[i][j][0] = h
			im[i][j][1] = s
			im[i][j][2] = v

def convertToGrayscale(img):
	w = len(img[0])
	h = len(img)
	res = []
	for i in range(h):
		row = []
		for j in range(w):
			row.append(int(0.299*img[i][j][0] + 0.587*img[i][j][1] + 0.114*img[i][j][2]))
		res.append(row)
	return res

def showimg(img):
	plt.imshow(img)
	plt.show()

def showGrayImg(img):
	plt.imshow(img, cmap='gray')
	plt.show()

def createimg(w, h):
	img = []
	for i in range(h):
		row = []
		for j in range(w):
			row.append([0,0,0])
		img.append(row)
	return img
	
def fillimg(img, r, g, b):
	r = len(img)
	c = len(img[0])
	for i in range(r):
		for j in range(c):
			img[i][j][0] = r
			img[i][j][1] = g
			img[i][j][2] = b
			
def fillrgb(img, br, bg, bb, w, h, p, step):
	for i in range(h):
		for j in range(w):
			for r in range(p):
				for c in range(p):
					img[i*p + r][j*p + c][0] = br + r * step
					img[i*p + r][j*p + c][1] = bg + c * step
					img[i*p + r][j*p + c][2] = bb + i * w * step + j * step
					
def fillhsv(img, hb, sb, vb, w, h, p):
	for i in range(h):
		for j in range(w):
			for r in range(p):
				for c in range(p):
					rr, gg, bb = hsvrgb(hb + i, sb + j/w, vb + r/p)					
					img[i*p + r][j*p + c][0] = rr
					img[i*p + r][j*p + c][1] = gg
					img[i*p + r][j*p + c][2] = bb

def histogram(maxa, maxb, maxc, nbina, nbinb, nbinc, img):
	res = {}
	n = len(img) * len(img[0])
	for i in range(len(img)):
		for j in range(len(img[0])):
			a = ceil(img[i][j][0] * nbina / maxa)
			b = ceil(img[i][j][1] * nbinb / maxb)
			c = ceil(img[i][j][2] * nbinc / maxc)
			h = a * nbinb * nbinc + b * nbinc + c
			if res.get(h) == None:
				res[h] = 1
			else:
				res[h] += 1
	for key in res:
		res[key] /= n
	return res
	
	
def simE(q, p):
	common = []
	sum = 0
	for key in q:
		if p.get(key) == None:
			continue
		sum = sum + (q[key] - p[key])*(q[key] - p[key])
		common.append(key)
	
	for key in q:
		if key in common:
			continue
		sum = sum + q[key] * q[key]
		
	for key in p:
		if key in common:
			continue
		sum = sum + p[key] * p[key]
	return sum

	
def simH(q, p):
	sum = 0
	sumq = 0
	for key in q:
		if p.get(key) == None:
			continue
		sum = sum + min(q[key], p[key])
		sumq += q[key]
	return sum / sumq

def openIm(file):
	im = Image.open(file)
	return copy(asarray(im))
	
def indexRGB(fld, n = -1):
	res = {}		
	for fname in listdir(fld):
		if n == 0:
			break
		n -= 1
		path = join(fld, fname)
		if not isfile(path):
			continue
		print(fname)
		im = openIm(path)
		res[fname] = histogram(255, 255, 255, 8, 8, 8, im)
	return res

def searchSimE(ind, file):
	q = ind[file]
	res = []
	for fname in ind:		
		res.append((fname, simE(q, ind[fname])))
	
	res = sorted(res, key = lambda item: item[1], reverse=False)	
	return res
	
def searchSimH(ind, file):
	q = ind[file]
	res = []
	for fname in ind:		
		res.append((fname, simH(q, ind[fname])))
	
	res = sorted(res, key = lambda item: item[1], reverse=True)
	return res
	
def showResult(docs, fld=IMFOLD, n = 10):
	for fname, score in docs:
		if n == 0:
			break
		n -= 1
		im = openIm(join(IMFOLD, fname))
		showimg(im)
'''
744.jpg
745.jpg
'''
