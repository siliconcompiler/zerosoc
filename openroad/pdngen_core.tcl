####################################
# grid for: core
####################################
define_pdn_grid -name {chip_core} -voltage_domains {CORE} -macro -cells "asic*" -halo "1.0 1.0 1.0 1.0"
add_pdn_connect -grid {chip_core} -layers {met4 met5}
