####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {_vdd} -ground {_vss}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE} -pins met4
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {5.44} -offset {0} -followpins
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch {27.140} -offset {13.570}
# Set to large pitch as the chip grid needs to be able to get met5 straps in too
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {160.000} -offset {80.000}
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
