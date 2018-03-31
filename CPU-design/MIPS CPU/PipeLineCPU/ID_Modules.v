`include "mux.v"
module NPC_jump (PC , Beq_offset , im_out , NPC_beq , NPC_j);
    input   [31:0]      PC;
    input   [31:0]      Beq_offset;
    input   [25:0]      im_out;
    
    output  [31:0]      NPC_beq;        
    output  [31:0]      NPC_j;          

    wire    [31:0]      w_PC;
    wire    [31:0]      w_Beq_offset;
    //PC+4
    assign w_PC = PC + 3'b100;
    //jump
    assign NPC_j[31:28] = w_PC[31:28];
    assign NPC_j[27:2] = im_out;
    assign NPC_j[1:0] = 2'b00;
    //Beq
    assign w_Beq_offset[31:2] = Beq_offset[29:0];
    assign w_Beq_offset[1:0] = 2'b0;
    assign NPC_beq = w_PC + w_Beq_offset;
endmodule

module RegFile ( A1 , A2 , WBdst , WD , RFWr , RD1 , RD2 ); 
    input  [4:0]     A1, A2, WBdst;
    input  [31:0]    WD;
    input            RFWr;
    output [31:0]    RD1, RD2;
    
    reg [31:0] regfile[31:0];
    integer i;

    initial begin           //初始化
        for (i=0; i<32; i=i+1)
            regfile[i] = 0;
    end

    always @( * )
    begin
        if (RFWr)
        begin
            regfile[WBdst] = WD;
        end
    end
    
    assign RD1 = (A1 == 0) ? 32'd0 : regfile[A1];
    assign RD2 = (A2 == 0) ? 32'd0 : regfile[A2];
endmodule

module Ext(Imm16, ExtOp, Imm32);
    input  [15:0] Imm16;
    input  [1:0]  ExtOp;
    output [31:0] Imm32;
    
    reg [31:0] Imm32;
        
    always @(*) begin
        case (ExtOp)
            2'b00:  Imm32 = {16'd0, Imm16}; //00
            2'b01:  Imm32 = {{16{Imm16[15]}}, Imm16}; //01
            2'b10:  Imm32 = {Imm16, 16'd0}; //10
            default: ;
        endcase
    end
endmodule