module regMEM_WB(MEM_DataMem ,MEM_RegW , rst,
            MEM_Reg_Src ,MEM_WBdst ,MEM_Alu_C ,
            clk ,WB_DataMem ,WB_RegW ,WB_Reg_Src ,
            WB_WBdst ,WB_Alu_C );

//DM
    input       [31:0]      MEM_DataMem;
//EXE_WB
    input                   MEM_RegW;
    input                   MEM_Reg_Src;
    input       [4:0]       MEM_WBdst;
    input       [31:0]      MEM_Alu_C;
//
    input                   clk;
    input                   rst;

    output  reg [31:0]      WB_DataMem;
    output  reg             WB_RegW;
    output  reg             WB_Reg_Src;
    output  reg [4:0]       WB_WBdst;
    output  reg [31:0]      WB_Alu_C;

    always @(posedge clk or posedge rst)
    begin
        if( rst )
        begin
            WB_DataMem = 32'b0;
            WB_RegW = 0;
            WB_Reg_Src = 0;
            WB_WBdst = 5'b0;
            WB_Alu_C = 32'b0;
        end
        else
        begin
            WB_DataMem = MEM_DataMem;
            WB_RegW = MEM_RegW;
            WB_Reg_Src = MEM_Reg_Src;
            WB_WBdst = MEM_WBdst;
            WB_Alu_C = MEM_Alu_C;
        end
    end
endmodule