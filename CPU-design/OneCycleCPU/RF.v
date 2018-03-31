`include "global_def.v"
module RF( A1, A2, A3, WD, clk, RFWr, RD1, RD2, RegDst );
    
   input  [4:0]  A1, A2, A3;
   input  [31:0] WD;
   input         clk;
   input         RFWr;
   input         RegDst;
   output [31:0] RD1, RD2;
   
   reg [31:0] rf[31:0];
   
   integer i;
   initial begin
       for (i=0; i<32; i=i+1)
          rf[i] = 0;
   end
   
   always @(posedge clk) begin
      if (RFWr & ~RegDst)
         rf[A3] <= WD;
      else if(RegDst)
         rf[A2] <= WD;
   end // end always
   
   assign RD1 = (A1 == 0) ? 32'd0 : rf[A1];
   assign RD2 = (A2 == 0) ? 32'd0 : rf[A2];
   
endmodule


