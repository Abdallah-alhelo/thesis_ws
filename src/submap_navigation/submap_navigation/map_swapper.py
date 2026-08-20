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

        # 2. Service Client to swap the map
        self.client = self.create_client(LoadMap, '/map_server/load_map')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Nav2 Map Server not available, waiting...')

        # 3. State Tracking
        self.current_submap = 'submap_1'  # We assume submap_1 is the main corridor

        # 4. Define Submap Geofences (Bounding Boxes in meters)
        # You will replace these dummy coordinates with the real ones from RViz
        self.zones = {
            'submap_2': {
                'x_min': 5.0, 'x_max': 8.5,
                'y_min': -3.0, 'y_max': -1.0,
                'yaml': '/home/iamalhelo103/thesis_ws/nav2_submaps/submap_2.yaml'
            },
            'submap_3': {
                'x_min': 8.6, 'x_max': 12.0,
                'y_min': -3.0, 'y_max': -1.0,
                'yaml': '/home/iamalhelo103/thesis_ws/nav2_submaps/submap_3.yaml'
            },
            # The corridor acts as the fallback map if the robot isn't inside any room
            'submap_1': {
                'yaml': '/home/iamalhelo103/thesis_ws/nav2_submaps/submap_1.yaml'
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
        target_submap = 'submap_1'  # Default to corridor

        for map_name, bounds in self.zones.items():
            if map_name == 'submap_1':
                continue # Skip the fallback map in the loop

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
