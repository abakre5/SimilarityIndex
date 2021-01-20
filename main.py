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

# In memory list of all images. Used natsorted, to have file list in proper order like 2.jpg, 3.jpg, etc unlike the
# python default behaviour 1.jpg, 11.jpg, 2.jpg to lower the repetitive calc of pairs like (2,3) and (3,2).
for image in ns.natsorted(glob.glob(IMAGE_REPO)):
    image_list.append(image)

# Finding similarity Index of all combination of images like (3.jpg,2.jpg), (4.jpg,2.jpg), (4.jpg,3.jpg),
# etc Not finding unnecessary similarity indices in cases like same image or like if index already calc for image
# pair 2 and 3 not again calculating for image 3 and image 2 combination. Hence, increasing efficiency.
i = 0
while i < len(image_list):
    j = 0
    primeImage = cv2.imread(image_list[i])
    # Converting to grayscale image to reduce noise in color images for better comparison
    grayPrimeImage = cv2.cvtColor(primeImage, cv2.COLOR_BGR2RGB)
    while j < len(image_list):
        if image_list[i] != image_list[j] and j >= i:
            refImage = cv2.imread(image_list[j])
            grayRefImage = cv2.cvtColor(refImage, cv2.COLOR_BGR2RGB)
            value = ssimage(grayPrimeImage, grayRefImage, multichannel=True, Full=True)
            mainImage.append(image_list[i].split("\\")[1])
            imageToCompare.append(image_list[j].split("\\")[1])
            similarityIndexList.append(value)
        j = j + 1
    i = i + 1

# Converting acquired data into object for csv export
csvObject = {
    'Image 1': mainImage,
    'Image 2': imageToCompare,
    'Similarity Index': similarityIndexList,
}

# CSV export
df = pd.DataFrame(csvObject)
df.to_csv(OUTPUT_CSV_FILENAME, index=False)