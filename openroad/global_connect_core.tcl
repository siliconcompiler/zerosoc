####################################
# global connections
####################################
add_global_connection -net {_vdd} -pin_pattern {VDD} -power
add_global_connection -net {_vdd} -pin_pattern {VPWR}
add_global_connection -net {_vdd} -pin_pattern {VPB}
add_global_connection -net {_vdd} -pin_pattern {vccd1}
add_global_connection -net {_vss} -pin_pattern {VSS} -ground
add_global_connection -net {_vss} -pin_pattern {VGND}
add_global_connection -net {_vss} -pin_pattern {VNB}
add_global_connection -net {_vss} -pin_pattern {vssd1}
