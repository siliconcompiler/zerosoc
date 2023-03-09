####################################
# grid for: sky130_sram_*
####################################
define_pdn_grid -name {SRAM} -voltage_domains {CORE} -macro -cells "sky130_sram_*" -halo "2.0 2.0 2.0 2.0"
add_pdn_connect -grid {SRAM} -layers {met4 met5}
