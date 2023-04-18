#read_liberty ../build/zerosoc_core/job0/export/1/outputs/zerosoc_core.slow.lib
read_liberty ../build/zerosoc_core/job0/syn/0/inputs/sc_dff_library.lib
read_liberty ../build/zerosoc_core/job0/syn/0/inputs/sc_logiclib_sky130hd_sky130_fd_sc_hd__ss_n40C_1v40.lib.lib
read_liberty ../build/zerosoc_core/job0/syn/0/inputs/sc_macrolib_sky130sram_sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib
read_verilog ../build/zerosoc_core/job0/export/1/outputs/asic_core.vg
link_design asic_core
#read_sdf ../build/zerosoc_core/job0/export/1/outputs/asic_core_slow.sdf
read_spef ../build/zerosoc_core/job0/export/1/outputs/asic_core.maximum.spef
#read_sdc -echo ../build/zerosoc_core/job0/export/1/outputs/asic_core.sdc
#report_checks
read_sdc ../build/zerosoc_core/job0/export/1/outputs/asic_core.sdc

report_checks

write_sdf asic_core.sdf
