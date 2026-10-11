import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from nav2_msgs.srv import LoadMap

class MapSwapperNode(Node):
    def __init__(self):
        super().__init__('map_swapper_node')

        # 1. TF2 Listener to track the robot's global position
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 2. Service Client to swap the local map 
        self.client = self.create_client(LoadMap, '/local_submap_server/load_map')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Nav2 Map Server not available, waiting...')

        # 3. State Tracking
        self.current_submap = 'submap_3'  # submap_3 is the main corridor

        # 4. Define Submap Geofences (Bounding Boxes in meters)
        # You will replace these dummy coordinates with the real ones from RViz
        self.zones = {
            'submap_1': {
                'x_min': -6.20, 'x_max': -2.65,
                'y_min': 15.5, 'y_max': 20.95,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_1.yaml'
            },
            'submap_2': {
                'x_min': 2.85, 'x_max': 6.35,
                'y_min': 15.5, 'y_max': 20.95,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_2.yaml'
            },
            'submap_4': {
                'x_min': -12.50, 'x_max': -5.65,
                'y_min': 12.4, 'y_max': 17.20,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_4.yaml'
            },
            'submap_5': {
                'x_min': 5.85, 'x_max': 12.55,
                'y_min': 12.2, 'y_max': 17.20,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_5.yaml'
            },
            'submap_6': {
                'x_min': -12.50, 'x_max': -9.5,
                'y_min': 8.25, 'y_max': 12.20,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_6.yaml'
            },
            'submap_7': {
                'x_min': 9.4, 'x_max': 12.55,
                'y_min': 8.30, 'y_max': 12.20,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_7.yaml'
            },
            'submap_8': {
                'x_min': -12.50, 'x_max': -9.4,
                'y_min': 3.75, 'y_max': 7.75,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_8.yaml'
            },
            'submap_9': {
                'x_min': 9.4, 'x_max': 11.85,
                'y_min': 3.75, 'y_max': 7.40,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_9.yaml'
            },
            'submap_10': {
                'x_min': -12.50, 'x_max': -6.9,
                'y_min': -10.25, 'y_max': 4.25,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_10.yaml'
            },
            'submap_11': {
                'x_min': 6.85, 'x_max': 12.55,
                'y_min': -10.25, 'y_max': 4.00,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_11.yaml'
            },
            'submap_12': {
                'x_min': 0.15, 'x_max': 3.3,
                'y_min': -6.30, 'y_max': -0.3,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_12.yaml'
            },
            'submap_13': {
                'x_min': -3.20, 'x_max': -0.2,
                'y_min': -6.35, 'y_max': -0.3,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_13.yaml'
            },
            'submap_14': {
                'x_min': -12.50, 'x_max': -6.9,
                'y_min': -24.20, 'y_max': -9.75,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_14.yaml'
            },
            'submap_15': {
                'x_min': -3.30, 'x_max': 0.20,
                'y_min': -13.25, 'y_max': -10.3,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_15.yaml'
            },
            'submap_16': {
                'x_min': -0.15, 'x_max': 3.40,
                'y_min': -13.25, 'y_max': -10.3,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_16.yaml'
            },
            'submap_17': {
                'x_min': 6.80, 'x_max': 12.55,
                'y_min': -24.25, 'y_max': -9.80,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_17.yaml'
            },
            'submap_18': {
                'x_min': -3.70, 'x_max': 0.30,
                'y_min': -23.25, 'y_max': -16.4,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_18.yaml'
            },
            'submap_19': {
                'x_min': -0.20, 'x_max': 3.80,
                'y_min': -23.25, 'y_max': -16.4,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_19.yaml'
            },
            'submap_20': {
                'x_min': -12.50, 'x_max': -6.75,
                'y_min': -31.70, 'y_max': -23.75,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_20.yaml'
            },
            'submap_21': {
                'x_min': -3.65, 'x_max': 12.55,
                'y_min': -31.70, 'y_max': -25.20,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_21.yaml'
            },
            # The corridor acts as the fallback map if the robot isn't inside any room
            'submap_3': {
            	'x_min': -12.50, 'x_max': 12.55,
                'y_min': -35, 'y_max': 17.85,
                'yaml': '/home/iamalhelo103/thesis_ws/src/submap_navigation/maps/nav2_submaps/submap_3.yaml'
            }
        }

        # 5. Timer to check position every 1 second (1.0 Hz)
        self.timer = self.create_timer(1.0, self.check_position)
        self.get_logger().info('Map Swapper Node Started. Tracking robot pose...')

    def check_position(self):
        try:
            # Get the mathematical transform from the 'map' frame to the robot's 'base_link'
            t = self.tf_buffer.lookup_transform(
                'map',
                'base_link',
                rclpy.time.Time())
        except (LookupException, ConnectivityException, ExtrapolationException):
            return

        x = t.transform.translation.x
        y = t.transform.translation.y

        # Determine which zone the robot is currently in
        target_submap = 'submap_3'  # Default to corridor

        for map_name, bounds in self.zones.items():
            #if map_name == 'submap_3':
             #   continue # Skip the fallback map in the loop

            # Check if the robot's X and Y are inside this room's bounding box
            if bounds['x_min'] <= x <= bounds['x_max'] and bounds['y_min'] <= y <= bounds['y_max']:
                target_submap = map_name
                break

        # If the robot entered a new zone, trigger the map swap!
        if target_submap != self.current_submap:
            self.get_logger().info(f'Crossed boundary! Switching from {self.current_submap} to {target_submap}')
            self.swap_map(target_submap)

    def swap_map(self, map_name):
        yaml_path = self.zones[map_name]['yaml']
        req = LoadMap.Request()
        req.map_url = yaml_path

        # Call the Nav2 service asynchronously so we don't freeze the node
        future = self.client.call_async(req)
        future.add_done_callback(self.map_swap_callback)
        self.current_submap = map_name

    def map_swap_callback(self, future):
        try:
            response = future.result()
            if response.result == 0:  # 0 indicates success in Nav2
                self.get_logger().info(f'Successfully loaded {self.current_submap}!')
            else:
                self.get_logger().error('Nav2 rejected the map swap.')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = MapSwapperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
