module zerosoc #(
  parameter bit IbexPipeLine = 0,
  parameter [31:0] BootAddr = 32'b0,
  // TODO: need to hard code file until https://github.com/zachjs/sv2v/issues/147 is resolved
  parameter RamInitFile = "sw/hello.mem",
  parameter RamDepth = 512
) (
  // Clock and Reset
  input        clk_i,
  input        rst_ni,

  input        uart_rx_i,
  output logic uart_tx_o,
  output logic uart_tx_en_o,

  input  [31:0] gpio_i,
  output [31:0] gpio_o,
  output [31:0] gpio_en_o
);

  import tlul_pkg::*;

  tl_h2d_t  tl_corei_h_h2d;
  tl_d2h_t  tl_corei_h_d2h;

  tl_h2d_t  tl_cored_h_h2d;
  tl_d2h_t  tl_cored_h_d2h;

  tl_h2d_t  tl_uart_d_h2d;
  tl_d2h_t  tl_uart_d_d2h;

  tl_h2d_t  tl_gpio_d_h2d;
  tl_d2h_t  tl_gpio_d_d2h;

  tl_h2d_t tl_ram_d_h2d;
  tl_d2h_t tl_ram_d_d2h;

  tl_h2d_t tl_xbar_h_h2d;
  tl_d2h_t tl_xbar_h_d2h;

  tl_dbg cored_dbg (
    .tl_h2d(tl_cored_h_h2d),
    .tl_d2h(tl_cored_h_d2h)
  );

  rv_core_ibex #(
    .PMPEnable                (0),
    .PMPGranularity           (0), // 2^(PMPGranularity+2) == 4 byte granularity
    .PMPNumRegions            (16),
    .MHPMCounterNum           (0),
    .MHPMCounterWidth         (0),
    .RV32E                    (0),
    .RV32M                    (ibex_pkg::RV32MNone),
    .RV32B                    (ibex_pkg::RV32BNone),
    .RegFile                  (ibex_pkg::RegFileFPGA),
    .BranchTargetALU          (0),
    .WritebackStage           (0),
    .ICache                   (0),
    .ICacheECC                (0),
    .BranchPredictor          (0),
    .DbgTriggerEn             (0),
    .SecureIbex               (0),
    // .DmHaltAddr               (ADDR_SPACE_DEBUG_MEM + dm::HaltAddress[31:0]),
    // .DmExceptionAddr          (ADDR_SPACE_DEBUG_MEM + dm::ExceptionAddress[31:0]),
    .PipeLine                 (IbexPipeLine)
  ) u_rv_core_ibex (
    // clock and reset
    .clk_i                (clk_i),
    .rst_ni               (rst_ni),
    // Don't use "escalation receiver"
    .clk_esc_i            (1'b0),
    .rst_esc_ni           (1'b1),

    // Unused when ICache is off
    .ram_cfg_i            ({$bits(prim_ram_1p_pkg::ram_1p_cfg_t){1'b0}}),

    // static pinning
    .hart_id_i            (32'b0),
    .boot_addr_i          (BootAddr),

    // TL-UL buses
    .tl_i_o               (tl_corei_h_h2d),
    .tl_i_i               (tl_corei_h_d2h),
    .tl_d_o               (tl_cored_h_h2d),
    .tl_d_i               (tl_cored_h_d2h),

    // interrupts
    .irq_software_i       (1'b0),
    .irq_timer_i          (1'b0),
    .irq_external_i       (1'b0),

    // escalation input from alert handler (NMI)
    .esc_tx_i             (1'b0),
    .esc_rx_o             (),

    // debug interface
    .debug_req_i          (1'b0),

    // crash dump interface
    .crash_dump_o         (),

    // CPU control signals -- stay running
    .lc_cpu_en_i          (lc_ctrl_pkg::On),
    .pwrmgr_cpu_en_i      (lc_ctrl_pkg::On),
    .core_sleep_o         (),

    // stay out of test mode
    .scan_rst_ni(1'b1),
    .scanmode_i(1'b0)
  );

  // sram device
  logic        ram_req;
  logic        ram_we;
  logic [10:0] ram_addr;
  logic [31:0] ram_wdata;
  logic [31:0] ram_wmask;
  logic [31:0] ram_rdata;
  logic        ram_rvalid;

  tlul_adapter_sram #(
    .SramAw($clog2(RamDepth)),
    .SramDw(32),
    .Outstanding(1),
    .EnableRspIntgGen(1),
    .EnableDataIntgGen(1)
  ) tl_adapter_ram (
    .clk_i   (clk_i),
    .rst_ni   (rst_ni),
    .tl_i     (tl_ram_d_h2d),
    .tl_o     (tl_ram_d_d2h),
    .en_ifetch_i(tlul_pkg::InstrEn),  // enable requests with "Instruction" type

    .req_o    (ram_req),
    .req_type_o(),
    .gnt_i    (1'b1), // Always grant as only one requester exists
    .we_o     (ram_we),
    .addr_o   (ram_addr),
    .wdata_o  (ram_wdata),
    .wmask_o  (ram_wmask),
    .intg_error_o(),
    .rdata_i  (ram_rdata),
    .rvalid_i (ram_rvalid),
    .rerror_i (2'b00)
  );

  prim_ram_1p_adv #(
    .Width(32),
    .Depth(RamDepth),
    .DataBitsPerMask(8),
    .MemInitFile(RamInitFile)
  ) ram (
    .clk_i    (clk_i),
    .rst_ni   (rst_ni),

    .req_i    (ram_req),
    .write_i  (ram_we),
    .addr_i   (ram_addr),
    .wdata_i  (ram_wdata),
    .wmask_i  (ram_wmask),
    .rdata_o  (ram_rdata),
    .rvalid_o (ram_rvalid),
    .rerror_o (), // tied to zero, not important

    .cfg_i(8'b0) // currently unused
  );

  gpio gpio (
      .clk_i (clk_i),
      .rst_ni (rst_ni),

      // Input
      .cio_gpio_i    (gpio_i),

      // Output
      .cio_gpio_o    (gpio_o),
      .cio_gpio_en_o (gpio_en_o),

      // Interrupt
      .intr_gpio_o (),

      // Inter-module signals
      .tl_i(tl_gpio_d_h2d),
      .tl_o(tl_gpio_d_d2h)
  );

  uart uart (
      .tl_i (tl_uart_d_h2d),
      .tl_o (tl_uart_d_d2h),

      // Input
      .cio_rx_i    (uart_rx_i),

      // Output
      .cio_tx_o    (uart_tx_o),
      .cio_tx_en_o (uart_tx_en_o),

      // Interrupt
      .intr_tx_watermark_o  (intr_uart_tx_watermark),
      .intr_rx_watermark_o  (intr_uart_rx_watermark),
      .intr_tx_empty_o      (intr_uart_tx_empty),
      .intr_rx_overflow_o   (intr_uart_rx_overflow),
      .intr_rx_frame_err_o  (intr_uart_rx_frame_err),
      .intr_rx_break_err_o  (intr_uart_rx_break_err),
      .intr_rx_timeout_o    (intr_uart_rx_timeout),
      .intr_rx_parity_err_o (intr_uart_rx_parity_err),

      .clk_i (clk_i),
      .rst_ni (rst_ni)
  );

  xbar xbar (
    .clk_i (clk_i),
    .rst_ni (rst_ni),

    // host interfaces
    .tl_corei_i     (tl_corei_h_h2d),
    .tl_corei_o     (tl_corei_h_d2h),
    .tl_cored_i     (tl_cored_h_h2d),
    .tl_cored_o     (tl_cored_h_d2h),

    // device interfaces
    .tl_ram_i       (tl_ram_d_d2h),
    .tl_ram_o       (tl_ram_d_h2d),
    .tl_uart_i      (tl_uart_d_d2h),
    .tl_uart_o      (tl_uart_d_h2d),
    .tl_gpio_i      (tl_gpio_d_d2h),
    .tl_gpio_o      (tl_gpio_d_h2d)
  );

endmodule
