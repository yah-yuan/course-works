`include "mux.v"
module DataMem( addr, din, DMWr, dout ,MEMW_src ,WB_data );
   input  [9:0] addr;
   input  [31:0] din;
   input         DMWr;
   input          MEMW_src;
   input  [31:0]  WB_data;
   output [31:0] dout;

   wire    [31:0] r_din;
   assign   r_din = MEMW_src ? WB_data : din;
   reg [31:0] dmem[1023:0];
   
   always @( * ) 
   begin
      if (DMWr)
         dmem[addr] <= r_din;
   end
   assign dout = dmem[addr]; 
endmodule    
