#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "gazebo_map_creator_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_map_creator_interface__srv__MapRequest_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_map_creator_interface__rosidl_generator_c")]
extern "C" {
    fn gazebo_map_creator_interface__srv__MapRequest_Request__init(msg: *mut MapRequest_Request) -> bool;
    fn gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Request>, size: usize) -> bool;
    fn gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Request>);
    fn gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MapRequest_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Request>) -> bool;
}

// Corresponds to gazebo_map_creator_interface__srv__MapRequest_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapRequest_Request {
    /// Request to send for map creation
    pub lowerright: geometry_msgs::msg::rmw::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub upperleft: geometry_msgs::msg::rmw::Point,

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
    pub filename: rosidl_runtime_rs::String,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_map_creator_interface__srv__MapRequest_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_map_creator_interface__srv__MapRequest_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MapRequest_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MapRequest_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MapRequest_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_map_creator_interface/srv/MapRequest_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_map_creator_interface__srv__MapRequest_Request() }
  }
}


#[link(name = "gazebo_map_creator_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_map_creator_interface__srv__MapRequest_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_map_creator_interface__rosidl_generator_c")]
extern "C" {
    fn gazebo_map_creator_interface__srv__MapRequest_Response__init(msg: *mut MapRequest_Response) -> bool;
    fn gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Response>, size: usize) -> bool;
    fn gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Response>);
    fn gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MapRequest_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MapRequest_Response>) -> bool;
}

// Corresponds to gazebo_map_creator_interface__srv__MapRequest_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MapRequest_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_map_creator_interface__srv__MapRequest_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_map_creator_interface__srv__MapRequest_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MapRequest_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_map_creator_interface__srv__MapRequest_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MapRequest_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MapRequest_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_map_creator_interface/srv/MapRequest_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_map_creator_interface__srv__MapRequest_Response() }
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


