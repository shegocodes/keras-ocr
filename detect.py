import argparse
import math, keras_ocr

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, 
					help='path to image')
parser.add_argument('--thresh', type=int, default=15, 
					help='threshold to distinguish new rows')
parser.add_argument('--order', type=str, default='yes', 
					help='enter y or yes to order detections in a human readable way')
args = parser.parse_args()

def detect_w_keras(image_path):
	"""Function returns detected text from image"""

	# Initialize pipeline
	pipeline = keras_ocr.pipeline.Pipeline()

	# Read in image path
	read_image = keras_ocr.tools.read(image_path)

	# prediction_groups is a list of (word, box) tuples
	prediction_groups = pipeline.recognize([read_image]) 

	return prediction_groups[0]


def get_distance(predictions):
	"""
	Function returns list of dictionaries with (key,value):
		* text : detected text in image
		* center_x : center of bounding box (x)
		* center_y : center of bounding box (y)
		* distance_from_origin : hypotenuse
		* distance_y : distance between y and origin (0,0)
	...for each bounding box (detections). 
	"""

	# Point of origin
	x0, y0 = 0, 0 

	# Generate dictionary
	detections = []
	for group in predictions:
		
		# Get center point of bounding box
		top_left_x, top_left_y = group[1][0]
		bottom_right_x, bottom_right_y = group[1][1]
		center_x, center_y = (top_left_x + bottom_right_x)/2, (top_left_y + bottom_right_y)/2
	
		# Use the Pythagorean Theorem to solve for distance from origin
		distance_from_origin = math.dist([x0,y0], [center_x, center_y])

		# Calculate difference between y and origin to get unique rows
		distance_y = center_y - y0
		
		# Append all results
		detections.append({
							'text': group[0], 
							'center_x': center_x, 
							'center_y': center_y, 
							'distance_from_origin': distance_from_origin,
							'distance_y': distance_y
						})
	
	return detections 


def distinguish_rows(lst, thresh=15):
	"""Function to help distinguish unique rows"""
	sublists = []
	for i in range(0, len(lst)-1):
		if (lst[i+1]['distance_y'] - lst[i]['distance_y'] <= thresh):
			if lst[i] not in sublists:
				sublists.append(lst[i])
			sublists.append(lst[i+1])
		else:
			yield sublists
			sublists = [lst[i+1]]
	yield sublists

def main(image_path, order='yes'):
	"""Function returns predictions from left to right & top to bottom"""
	predictions = detect_w_keras(image_path)
	predictions = get_distance(predictions)
	predictions = list(distinguish_rows(predictions, thresh=15))
	
	# Remove all empty rows
	predictions = list(filter(lambda x:x!=[], predictions))

	# Order text detections in human readable format
	ordered_preds = []
	ylst = ['yes', 'y']
	for row in predictions:
		if order in ylst: row = sorted(row, key=lambda x:x['distance_from_origin'])
		for each in row: ordered_preds.append(each['text'])
	
	return ordered_preds

if __name__=='__main__':
	
	image = args.image
	thresh = args.thresh
	order = args.order
	
	print(f'Generating predictions for {image}...')
	predictions = main(image, order)
	print(predictions)



	
