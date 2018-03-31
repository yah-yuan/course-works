`include "ctrl_encode_def.v"
module alu (A, B, ALUOp, C, Zero);
           
   input  [31:0] A, B;
   input  [3:0]  ALUOp;
   output reg [31:0] C;
   output        Zero;
       
   always @( A or B or ALUOp ) begin
      case ( ALUOp )
         `ALUOp_ADD: C = A + B;             //加
         `ALUOp_SUB: C = A - B;             //减
         `ALUOp_OR:  C = A | B;             //或
      endcase
   end 
   assign Zero = (A == B) ? 1 : 0;
endmodule
    