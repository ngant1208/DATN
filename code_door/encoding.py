# import face_recognition
from imutils import paths
import Face
import argparse
import pickle
import cv2
import os
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", default="dataset",
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", default="end.pickle",
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
knownEncodings = []
knownNames = []
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	boxes = Face.face_locations(rgb,
		model=args["detection_method"])
	# compute the facial embedding for the face
	encodings = Face.face_encodings(rgb, boxes)
	# loop over the encodings
	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()