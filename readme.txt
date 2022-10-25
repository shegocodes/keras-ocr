# Purpose:
Improve Keras-OCR to read detected texts in a more 'human' way, 
meaning from left to right and top to bottom. 

# Install all necessary libraries
pip install -r requirements.txt

Full Explanation:  

Sample Runs: 

# Raw detection (order does not matter)
python detect.py --image images/wanderer.png --thresh 10 --order no

# Tighten threshold
python detect.py --image images/wanderer.png --thresh 10 --order yes
	
# Average threshold
python detect.py --image images/wanderer.png --thresh 15 --order yes 

# Loosen threshold
python detect.py --image images/wanderer.png --thresh 20 --order yes


