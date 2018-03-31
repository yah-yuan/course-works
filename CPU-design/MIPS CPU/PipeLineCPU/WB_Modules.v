`include "mux.v"
module ChoseDataWrite(Alu_C ,MemRead ,RegW_Src ,clk ,WriteData);
    input   [31:0]      Alu_C;
    input   [31:0]      MemRead;
    input               RegW_Src;
    input               clk;
    output  reg[31:0]   WriteData;

    wire    [31:0]      r_WriteData;

    mux2 U_mux2(
            .d0(Alu_C),
            .d1(MemRead),
            .s(RegW_Src),
            .y(r_WriteData)
    );
    
    always @(negedge clk)
    begin
        WriteData = r_WriteData;
    end
endmodule
