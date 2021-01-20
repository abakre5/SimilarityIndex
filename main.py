from skimage.metrics import structural_similarity as ssimage

import glob
import cv2
import pandas as pd
import natsort as ns

IMAGE_REPO = 'ImageRepo\*';
OUTPUT_CSV_FILENAME = 'SimilarityIndex.csv';

# Contains filepath of all the images to be compared
image_list = []

# Store list of image, image to compare and similarity index of the pair
mainImage = []
imageToCompare = []
similarityIndexList = []

# In memory list of all images
for image in ns.natsorted(glob.glob(IMAGE_REPO)):
    image_list.append(image)

# Finding similarity Index of all combination of images like (2.jpg,3.jpg), (2.jpg,4.jpg), (2.jpg,5.jpg), etc
i = 0
while i < len(image_list):
    j = 0
    primeImage = cv2.imread(image_list[i])
    grayPrimeImage = cv2.cvtColor(primeImage, cv2.COLOR_BGR2RGB)
    while j < len(image_list):
        if image_list[i] != image_list[j] and j <= i:
            refImage = cv2.imread(image_list[j])
            grayRefImage = cv2.cvtColor(refImage, cv2.COLOR_BGR2RGB)
            value = ssimage(grayPrimeImage, grayRefImage, multichannel=True, Full=True)
            mainImage.append(image_list[i])
            imageToCompare.append(image_list[j])
            similarityIndexList.append(value)
            print(image_list[i], " -> ", image_list[j], "->", value)
        j = j + 1
    i = i + 1

outputObj = {
    'Image1': mainImage,
    'Image2': imageToCompare,
    'SimilarityIndex': similarityIndexList,
}

df = pd.DataFrame(outputObj)
df.to_csv(OUTPUT_CSV_FILENAME)