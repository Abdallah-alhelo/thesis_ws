import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/iamalhelo103/thesis_ws/install/submap_navigation'
