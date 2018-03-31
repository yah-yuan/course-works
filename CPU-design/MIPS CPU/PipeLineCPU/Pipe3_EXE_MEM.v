module regEXE_MEM(MEM_RegW , MEM_RegW_Src , MEM_MemW , MEM_WBdst, 
                MEM_instrOp , clk , rst , EXE_RegW , EXE_RegW_Src,
                EXE_MemW , EXE_WBdst , EXE_instrOp ,EXE_Alu_C ,MEM_Alu_C,
                EXE_RegFileB ,MEM_RegFileB,EXE_RegFileA,MEM_RegFileA,
                EXE_MEMW_src,MEM_MEMW_src);

//ID_EXE
    input                       EXE_RegW;			//寄存器堆写入数据，为1写，否则不写
    input                       EXE_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
    input                       EXE_MemW;			//写数据存储器	
    input       [4:0]	        EXE_WBdst;			//目标寄存器
    input       [5:0]		    EXE_instrOp;		//本条指令Op
    input       [31:0]          EXE_RegFileB;
    input       [31:0]          EXE_RegFileA;
    input                       EXE_MEMW_src;
//Alu
    input       [31:0]          EXE_Alu_C;
//
    input                       clk;
    input                       rst;
//out
    output reg                  MEM_RegW;
    output reg                  MEM_RegW_Src;
    output reg                  MEM_MemW;
    output reg  [4:0]	        MEM_WBdst;
    output reg  [5:0]		    MEM_instrOp;
    output reg  [31:0]          MEM_Alu_C;
    output reg  [31:0]          MEM_RegFileB;
    output reg  [31:0]          MEM_RegFileA;
    output reg                  MEM_MEMW_src;
    always @(posedge clk or posedge rst)
    begin
        if( rst )
        begin
            MEM_RegW = 0;
            MEM_RegW_Src = 0;
            MEM_MemW = 0;
            MEM_WBdst = 5'b0;
            MEM_instrOp = 6'b0;
            MEM_Alu_C = 32'b0;
            MEM_RegFileB = 32'b0;
            MEM_RegFileA = 32'b0;
            MEM_MEMW_src = 0;
        end
        else
        begin
            MEM_RegW = EXE_RegW;
            MEM_RegW_Src = EXE_RegW_Src;
            MEM_MemW = EXE_MemW;
            MEM_WBdst = EXE_WBdst;
            MEM_instrOp = EXE_instrOp;
            MEM_Alu_C = EXE_Alu_C;
            MEM_RegFileB = EXE_RegFileB;
            MEM_RegFileA = EXE_RegFileA;
            MEM_MEMW_src = EXE_MEMW_src;
        end
    end
endmodule