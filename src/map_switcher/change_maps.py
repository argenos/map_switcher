from os.path import join

import rospy
import roslaunch
import rosnode
import tf

from map_switcher.srv import SwitchMap, SwitchMapResponse
from geometry_msgs.msg import PoseWithCovarianceStamped

class MapSwitcher(object):
    def __init__(self, map_dir, map_switcher_server='~change_map'):
        self.map_dir = map_dir
        self.map_switcher_server = map_switcher_server
        self.default_map = rospy.get_param('~default_map', 'basement-full')
        self.building_name = rospy.get_param('~building', 'amk')
        self.maps = rospy.get_param('~maps', '')
        self.wormholes = rospy.get_param('~wormholes', '')

        rospy.init_node('map_switcher', anonymous=True)

        self.uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(self.uuid)

        # Setup the package and executable we want to launch
        self.package = 'map_server'
        self.executable = 'map_server'
        args = join(self.map_dir, self.building_name, self.default_map + "/map.yaml")

        # TODO Only launch the map_server if it's not already there
        # Also, we asume the name of the server is indeed map_server
        node = roslaunch.core.Node(self.package, self.executable, name='map_server', args=args)

        self.launch = roslaunch.scriptapi.ROSLaunch()
        self.launch.start()

        self.map_server = self.launch.launch(node)

        self.server = rospy.Service(self.map_switcher_server, SwitchMap, self.handle_map_req)

        rospy.loginfo("Initialized map_switcher")


    def handle_map_req(self, req):
        rospy.loginfo("Received request to switch to %s map" % req.new_map)
        reply = SwitchMapResponse()

        if req.new_map not in self.maps:
            reply.success = False
            rospy.logerr("This map was not specified in the config file. Aborting...")
            return reply

        if not self.wormholes.has_key(req.entry_wormhole):
            reply.success = False
            rospy.logerr("This wormhole was not specified in the config file. Aborting...")
            return reply

        rosnode.kill_nodes('map_server')
        rospy.sleep(1)

        map_name = req.new_map
        wormhole = req.entry_wormhole

        #TODO robustly handle directories /
        args = join(self.map_dir, self.building_name, map_name + '/map.yaml')

        node = roslaunch.core.Node(self.package, self.executable, name='map_server', args=args)

        self.map_server = self.launch.launch(node)

        reply.success = True

        reply.estimated_pose.pose.pose.position.x = self.wormholes[wormhole]['connected_locations'][map_name]['position'][0]
        reply.estimated_pose.pose.pose.position.y = self.wormholes[wormhole]['connected_locations'][map_name]['position'][1]
        reply.estimated_pose.pose.pose.position.z = 0.0

        orientation = tf.transformations.quaternion_from_euler(0.0, 0.0, self.wormholes[wormhole]['connected_locations'][map_name]['orientation'])
        reply.estimated_pose.pose.pose.orientation.x = orientation[0]
        reply.estimated_pose.pose.pose.orientation.y = orientation[1]
        reply.estimated_pose.pose.pose.orientation.z = orientation[2]
        reply.estimated_pose.pose.pose.orientation.w = orientation[3]

        reply.estimated_pose.pose.covariance = [0.0]*36


        return reply
