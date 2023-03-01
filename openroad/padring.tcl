
# Create false IO sites, since sky130 does not have PAD sites available
make_fake_io_site -name IO_HSITE -width 1 -height 200
make_fake_io_site -name IO_VSITE -width 1 -height 200
make_fake_io_site -name IO_CSITE -width 200 -height 204

# Create IO Rows
make_io_sites -horizontal_site IO_HSITE -vertical_site IO_VSITE -corner_site IO_CSITE -offset 10 -rotation R180


proc place_pad {args} {
    puts $args
  sta::parse_key_args "place_pad" args \
    keys {-master -location -row} \
    flags {-mirror}

  sta::check_argc_eq1 "place_pad" $args

  set master "NULL"
  if {[info exists keys(-master)]} {
    set master [pad::find_master $keys(-master)]
  }
  set name [lindex $args 0]
  pad::assert_required place_pad -location
  set offset [ord::microns_to_dbu $keys(-location)]

  pad::assert_required place_pad -row
  puts $name
  pad::place_pad $master \
                 $name \
                 [pad::get_row $keys(-row)] \
                 $offset \
                 [info exists flags(-mirror)]
}


# Place pads
proc place_padring_edge { row dim edge } {
    upvar sc_cfg  sc_cfg
    upvar sc_tool sc_tool
    upvar sc_task sc_task
    set span [ord::dbu_to_microns [[[pad::get_row $row] getBBox] d$dim]]
    set span_start [ord::dbu_to_microns [[[pad::get_row $row] getBBox] ${dim}Min]]
    set pad_length [llength [dict get $sc_cfg tool $sc_tool task $sc_task {var} padring_${edge}_name]]
    set pad_interval [expr $span / ($pad_length + 1)]
    for { set i 0 } { $i < $pad_length } { incr i } {
        set pad_name   [lindex [dict get $sc_cfg tool $sc_tool task $sc_task {var} padring_${edge}_name] $i]
        set pad_master [lindex [dict get $sc_cfg tool $sc_tool task $sc_task {var} padring_${edge}_master] $i]
        puts "Placing IO pad: $pad_name"
        place_pad \
            -master $pad_master \
            -row $row \
            -location [expr $span_start + ($i + 0.5) * $pad_interval] \
            $pad_name
    }
}

place_padring_edge IO_WEST y west
place_padring_edge IO_NORTH x north
place_padring_edge IO_EAST y east
place_padring_edge IO_SOUTH x south

# Place corners
place_corners sky130_ef_io__corner_pad

# Place IO fill
set iofill [dict get $sc_cfg library sky130io asic cells filler]
place_io_fill -row IO_NORTH {*}$iofill
place_io_fill -row IO_SOUTH {*}$iofill
place_io_fill -row IO_WEST {*}$iofill
place_io_fill -row IO_EAST {*}$iofill

# Connect ring signals
connect_by_abutment

# Add bond pads
place_bondpad -bond sky130_ef_io__bare_pad padring.*_pads\[0\].i0.*.gpio -offset "12.5 115"
place_bondpad -bond sky130_ef_io__bare_pad padring.*_pads\[0\].i0.*.io* -offset "8 95"
