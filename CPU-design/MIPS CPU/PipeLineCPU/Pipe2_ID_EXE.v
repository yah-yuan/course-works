module regID_EXE(ID_RegW , ID_RegW_Src , ID_MemW , 	ID_AluAsrc , 	
                ID_AluBsrc , ID_Aluctrl , ID_stopNext , ID_WBdst , 			
                ID_instrOp , ID_RegFileA , ID_RegFileB , ID_Imm32,
                clk, rst,ID_MEMW_src,EXE_MEMW_src,
                EXE_RegW , EXE_RegW_Src , EXE_MemW , EXE_AluAsrc , 	
                EXE_AluBsrc , EXE_Aluctrl , EXE_stopNext , EXE_WBdst , 			
                EXE_instrOp , EXE_RegFileA , EXE_RegFileB , EXE_Imm32);
//Ctrl in
    input                   ID_RegW;			//寄存器堆写入数据，为1写，否则不写
	input                   ID_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
	input                   ID_MemW;			//写数据存储器	
	input       [1:0]       ID_AluAsrc;		    //Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
	input       [1:0]		ID_AluBsrc;		    //运算器操作数选择
	input       [3:0] 		ID_Aluctrl;		    //Alu运算选择
	input                   ID_stopNext;		//是否废弃下一条指令
	input       [4:0]	    ID_WBdst;			//目标寄存器，传给ID_EXE
	input                   ID_MEMW_src;
    input       [5:0]		ID_instrOp;		    //本条指令Op，传给ID_EXE
//RegFile in
    input       [31:0]      ID_RegFileA;
    input       [31:0]      ID_RegFileB;
//Ext in
    input       [31:0]      ID_Imm32;   
//
    input                   clk;
    input                   rst;
//Ctrl out
    output  reg             EXE_RegW;			//寄存器堆写入数据，为1写，否则不写
	output  reg             EXE_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
	output  reg             EXE_MemW;			//写数据存储器	
	output  reg [1:0]       EXE_AluAsrc;		//Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
	output  reg [1:0]		EXE_AluBsrc;		//运算器操作数选择
	output  reg [3:0] 		EXE_Aluctrl;		//Alu运算选择
	output  reg             EXE_stopNext;		//是否废弃下一条指令
	output  reg [4:0]	    EXE_WBdst;			//目标寄存器，传给EXE_EXE
	output  reg [5:0]		EXE_instrOp;		//本条指令Op，传给EXE_EXE
    output  reg [31:0]      EXE_RegFileA;
    output  reg [31:0]      EXE_RegFileB;
    output  reg [31:0]      EXE_Imm32;      
    output  reg             EXE_MEMW_src;

    always @(posedge clk or posedge rst)
    begin
        if( rst )
        begin
            EXE_RegW = 0;	
            EXE_RegW_Src = 0;		
            EXE_MemW = 0;		
            EXE_AluAsrc = 2'b0;	
            EXE_AluBsrc = 2'b0;		
            EXE_Aluctrl = 4'b0;		
            EXE_stopNext = 0;		
            EXE_WBdst = 5'b0;			
            EXE_instrOp = 6'b0;
            EXE_RegFileA = 0;
            EXE_RegFileB = 0;
            EXE_Imm32 = 0;
            EXE_MEMW_src = 0;
        end
        else
        begin
            EXE_RegW = ID_RegW;
            EXE_RegW_Src = ID_RegW_Src;		
            EXE_MemW = ID_MemW;	
            EXE_AluAsrc = ID_AluAsrc;	
            EXE_AluBsrc = ID_AluBsrc;		
            EXE_Aluctrl = ID_Aluctrl;		
            EXE_stopNext = ID_stopNext;		
            EXE_WBdst = ID_WBdst;			
            EXE_instrOp = ID_instrOp;		
            EXE_RegFileA = ID_RegFileA;
            EXE_RegFileB = ID_RegFileB;
            EXE_Imm32 = ID_Imm32;
            EXE_MEMW_src = ID_MEMW_src;
        end
    end
endmodule