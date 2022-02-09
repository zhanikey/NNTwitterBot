import resnext

img_path = "submissions/2.jpg"
prediction = resnext.resnext_classify(img_path)
print(type(prediction[0]))