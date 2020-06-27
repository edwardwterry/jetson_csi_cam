#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CameraInfo
import yaml

calibration_file = '/home/ed/.ros/camera_info/camera.yaml'
with open(calibration_file, 'r') as f:
    data = yaml.safe_load(f)

def callback(msg):
    info = CameraInfo()
    info.header = msg.header
    info.height = data['image_height']
    info.width = data['image_width']
    info.distortion_model = data['distortion_model']
    info.D = data['distortion_coefficients']['data']
    info.K = data['camera_matrix']['data']
    info.P = data['projection_matrix']['data']
    info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    info_pub.publish(info)

if __name__ == '__main__':
    rospy.init_node('publish_camera_info', anonymous=True)
    image_sub = rospy.Subscriber('image_raw_throttle', Image, callback)
    info_pub = rospy.Publisher('camera_info', CameraInfo, queue_size=1)
    rospy.spin()