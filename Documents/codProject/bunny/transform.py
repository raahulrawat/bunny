import imutils
import time
import cv2


class Trans:

    def __init__(self):

        self.outputPath = "static/output/processed.png"


    def bunny(self, model, image):
        """
        :param model: selected model for transfer style
        :param image: uploaded image to create Art
        :return: retun the status of the process
        """
        isSuccess = False
        try:
            # load the neural style transfer model from disk
            print("[INFO] loading style transfer model...")
            print(model, image)
            net = cv2.dnn.readNetFromTorch(model)

            # load the input image, resize it to have a width of 600 pixels, and
            # then grab the image dimensions
            image = cv2.imread(image)
            image = imutils.resize(image, width=600)
            (h, w) = image.shape[:2]

            # construct a blob from the image, set the input, and then perform a
            # forward pass of the network
            blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
                                         (103.939, 116.779, 123.680), swapRB=False, crop=False)
            net.setInput(blob)
            start = time.time()
            output = net.forward()
            end = time.time()

            # reshape the output tensor, add back in the mean subtraction, and
            # then swap the channel ordering
            output = output.reshape((3, output.shape[2], output.shape[3]))
            output[0] += 103.939
            output[1] += 116.779
            output[2] += 123.680
            # output /= 255.0
            output = output.transpose(1, 2, 0)

            # show information on how long inference took
            print("[INFO] neural style transfer took {:.4f} seconds".format(
                end - start))

            cv2.imwrite(self.outputPath, output)
            isSuccess = True
            return isSuccess
        except:
            return isSuccess