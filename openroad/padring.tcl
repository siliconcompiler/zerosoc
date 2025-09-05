# Create false IO sites, since sky130 does not have PAD sites available
make_fake_io_site -name IO_SITE -width 1 -height 200
make_fake_io_site -name IO_CSITE -width 200 -height 204

# Create IO Rows
make_io_sites -horizontal_site IO_SITE -vertical_site IO_SITE -corner_site IO_CSITE -offset 10 \
    -rotation_horizontal R180 \
    -rotation_vertical R180 \
    -rotation_corner R180 \

# Place pads
proc soc_get_pad_cells {side} {
    set cells [get_cells -quiet */i${side}/ipad[*].*]

    set insts []
    set i 0
    while { [llength $insts] != [llength $cells] } {
        foreach type "gpio iovdd* iovss*" {
            set cell [get_cells -quiet */i${side}/ipad[$i].*/${type}]
            if {[llength $cell] != 0} {
                break
            }
        }
        incr i
        if { $i > 100 } {
            break
        }
        if {[llength $cell] == 0} {
            continue
        }
        lappend insts [[sta::sta_to_db_inst $cell] getName]
    }

    return $insts
}

# Handle north
puts "Place north edge"
place_pads -row IO_NORTH [soc_get_pad_cells north]

# Handle south
puts "Place south edge"
place_pads -row IO_SOUTH [soc_get_pad_cells south]

# Handle west
puts "Place west edge"
place_pads -row IO_WEST [lreverse [soc_get_pad_cells west]]

# Handle east
puts "Place east edge"
place_pads -row IO_EAST [lreverse [soc_get_pad_cells east]]

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
place_bondpad -bond sky130_ef_io__bare_pad padring/*.i0/gpio -offset "12.5 115"
place_bondpad -bond sky130_ef_io__bare_pad padring/*.i0/io* -offset "8 95"
