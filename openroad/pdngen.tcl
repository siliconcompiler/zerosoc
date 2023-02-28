####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {_vdd} -ground {_vss}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE}
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {5.44} -offset {0} -followpins
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch {27.140} -offset {13.570}
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {27.200} -offset {13.600}
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
####################################
# macro grids
####################################
####################################
# grid for: sky130_sram_*
####################################
define_pdn_grid -name {SRAM} -voltage_domains {CORE} -macro -cells "sky130_sram_*" -halo "2.0 2.0 2.0 2.0"
add_pdn_connect -grid {SRAM} -layers {met4 met5}
