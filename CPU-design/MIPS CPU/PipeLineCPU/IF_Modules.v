`include "mux.v"
module InsMem( addr, dout );
    
    input [9:0]     addr;
    output [31:0] dout;
    
    reg [31:0] imem[1023:0];
    reg [31:0]  dout;
    
    always @( addr )
    begin
        dout <= imem[addr];
    end
endmodule

module PC( clk, rst, PCWr, NPC, PC );       
    input         clk;
    input         rst;
    input         PCWr;
    input  [31:0] NPC;
    output [31:0] PC;
    
    reg [31:0] PC;
    reg [1:0] tmp;
                
    always @(posedge clk or posedge rst) 
    begin
        if ( rst ) 
            PC <= 32'h0000_3000;   
        else if ( PCWr ) 
            PC <= NPC;
    end          
endmodule

module NPC( NPC_4 , NPC_j , NPC_beq , NPCOp , NPC);
    input       [31:0]          NPC_4;
    input       [31:0]          NPC_j;
    input       [31:0]          NPC_beq;
    input       [1:0]           NPCOp;
    output      [31:0]          NPC;

    wire        [31:0]          temp;

    mux4 U_mux4(
        .d0(NPC_4),
        .d1(NPC_j),
        .d2(NPC_beq),
        .d3(temp),
        .s(NPCOp),
        .y(NPC)
    );
endmodule    