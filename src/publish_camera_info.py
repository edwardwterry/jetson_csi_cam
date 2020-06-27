#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import yaml
import numpy as np

calibration_file = '/home/ed/.ros/camera_info/camera.yaml'
with open(calibration_file, 'r') as f:
    data = yaml.safe_load(f)

br = CvBridge()

def callback(msg):
    camera_matrix = np.array(data['camera_matrix']['data']).reshape([3,3])
    distortion_coeffs = np.array(data['distortion_coefficients']['data'])
    im = cv2.undistort(br.imgmsg_to_cv2(msg), camera_matrix, distortion_coeffs)
    image_pub.publish(br.cv2_to_imgmsg(im, encoding='rgb8'))

if __name__ == '__main__':
    rospy.init_node('publish_camera_info', anonymous=True)
    image_sub = rospy.Subscriber('image_raw_throttle', Image, callback)
    image_pub = rospy.Publisher('image_rect_color_throttle', Image, queue_size=1)
    rospy.spin()