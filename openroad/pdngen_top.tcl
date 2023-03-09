####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {vdd} -ground {vss}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE}
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {5.44} -offset {0} -followpins
add_pdn_ring -connect_to_pads -layers {met4 met5} -widths {2.0 2.0} -spacings {2.0 2.0} -core_offsets {1.0 1.0 1.0 1.0}
add_pdn_ring -connect_to_pads -layers {met2 met3} -widths {2.0 2.0} -spacings {2.0 2.0} -core_offsets {1.0 1.0 1.0 1.0}
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch {27.140} -offset {13.570} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {27.200} -offset {13.600} -extend_to_core_ring
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met2 met3}
add_pdn_connect -grid {grid} -layers {met3 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
