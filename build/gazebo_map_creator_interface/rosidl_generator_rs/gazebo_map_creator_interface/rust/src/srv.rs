#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to gazebo_map_creator_interface__srv__MapRequest_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapRequest_Request {
    /// Request to send for map creation
    pub lowerright: geometry_msgs::msg::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub upperleft: geometry_msgs::msg::Point,

    /// Default is 2d map (e.g .pgm)
    pub skip_vertical_scan: u8,

    /// smaller the value, higher the resolution
    pub resolution: f64,

    /// Distance multiplier to check for horizontal collision.
    pub range_multiplier: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub threshold_2d: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filename: std::string::String,

}

impl MapRequest_Request {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MAP_2D: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MAP_3D: u8 = 1;

}


impl Default for MapRequest_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MapRequest_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MapRequest_Request {
  type RmwMsg = super::srv::rmw::MapRequest_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        lowerright: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.lowerright)).into_owned(),
        upperleft: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.upperleft)).into_owned(),
        skip_vertical_scan: msg.skip_vertical_scan,
        resolution: msg.resolution,
        range_multiplier: msg.range_multiplier,
        threshold_2d: msg.threshold_2d,
        filename: msg.filename.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        lowerright: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.lowerright)).into_owned(),
        upperleft: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.upperleft)).into_owned(),
      skip_vertical_scan: msg.skip_vertical_scan,
      resolution: msg.resolution,
      range_multiplier: msg.range_multiplier,
      threshold_2d: msg.threshold_2d,
        filename: msg.filename.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      lowerright: geometry_msgs::msg::Point::from_rmw_message(msg.lowerright),
      upperleft: geometry_msgs::msg::Point::from_rmw_message(msg.upperleft),
      skip_vertical_scan: msg.skip_vertical_scan,
      resolution: msg.resolution,
      range_multiplier: msg.range_multiplier,
      threshold_2d: msg.threshold_2d,
      filename: msg.filename.to_string(),
    }
  }
}


// Corresponds to gazebo_map_creator_interface__srv__MapRequest_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MapRequest_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MapRequest_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MapRequest_Response {
  type RmwMsg = super::srv::rmw::MapRequest_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}






#[link(name = "gazebo_map_creator_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_map_creator_interface__srv__MapRequest() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_map_creator_interface__srv__MapRequest
#[allow(missing_docs, non_camel_case_types)]
pub struct MapRequest;

impl rosidl_runtime_rs::Service for MapRequest {
    type Request = MapRequest_Request;
    type Response = MapRequest_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_map_creator_interface__srv__MapRequest() }
    }
}


