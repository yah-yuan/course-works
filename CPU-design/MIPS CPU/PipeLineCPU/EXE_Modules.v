`include "mux.v"
module Alu (A, B, ALUOp, C);         
    input  [31:0] A, B;
    input  [3:0]  ALUOp;
    output reg [31:0] C;
        
    always @( A or B or ALUOp ) 
    begin
        case ( ALUOp )
            4'b0000: C = A + B;             //加
            4'b0100: C = A - B;             //减
            4'b0101: C = A | B;             //或
        endcase
    end
endmodule

module AluA_src(RegFileA , EXE_AluC , MEM_WriteData , AluAsrc , AluA);
    input   [31:0]          RegFileA;
    input   [31:0]          EXE_AluC;
    input   [31:0]          MEM_WriteData;
    input   [1:0]           AluAsrc;
    output  [31:0]          AluA;

    wire    [31:0]          temp;

    mux4 U_mux4(
        .d0(RegFileA),
        .d1(EXE_AluC),
        .d2(MEM_WriteData),
        .d3(temp),
        .s(AluAsrc),
        .y(AluA)
    );
endmodule

module AluB_src(RegFileB , EXT_Imm32, EXE_AluC , MEM_WriteData , AluBsrc , AluB);
    input   [31:0]          RegFileB;
    input   [31:0]          EXT_Imm32;
    input   [31:0]          EXE_AluC;
    input   [31:0]          MEM_WriteData;
    input   [1:0]           AluBsrc;
    output  [31:0]          AluB;

    mux4 U_mux4(
        .d0(RegFileB),
        .d1(EXT_Imm32),
        .d2(EXE_AluC),
        .d3(MEM_WriteData),
        .s(AluBsrc),
        .y(AluB)
    );
endmodule
