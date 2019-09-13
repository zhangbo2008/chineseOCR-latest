# import cv2
# import matplotlib.pyplot as plt
# img = cv2.imread('lena.jpg')
# # img = img / 255.0

# rows, cols = img.shape[:2]
# #第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
# M1 = cv2.getRotationMatrix2D((cols/2, rows/2), 30, 1)
# M2 = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
# #第三个参数：变换后的图像大小
# res1 = cv2.warpAffine(img, M1, (rows, cols))
# res2 = cv2.warpAffine(img, M2, (rows, cols))
# cv2.imwrite('./ImageProcessed/rotated30_cv2.png', res1)
# cv2.waitKey()
# cv2.imwrite('./ImageProcessed/rotated90_cv2.png', res2)
# cv2.waitKey()
# cv2.imshow('Ori', img)
# cv2.waitKey()
# cv2.imshow('Rotated1', res1)
# cv2.waitKey()
# cv2.imshow('Rotated2', res2)
# cv2.waitKey()