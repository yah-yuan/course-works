module mips( clk, rst );
    input                       clk;
    input                       rst;
//IF
    //IM
    wire        [9:0]           IM_addr;
    wire        [31:0]          IM_dout;
    //PC
    wire                        PC_PCWr;
    wire        [31:0]          PC_NPC;
    wire        [31:0]          PC_PC;
    //NPC
    wire        [31:0]          NPC_NPC_4;
    wire        [31:0]          NPC_NPC_j;
    wire        [31:0]          NPC_NPC_beq;
    wire        [1:0]           NPC_NPCOp;
    wire        [31:0]          NPC_NPC;
    //regIF_ID
    wire        [31:0]          IF_ID_im_out;
    wire        [31:0]          IF_ID_PC;
    wire        [31:0]          IF_ID_IF_im_out;
    wire        [31:0]          IF_ID_IF_PC;
    wire                        IF_ID_IF_IDWr;
//ID
    //NPC_jump
    wire        [31:0]          NPC_jump_PC;
    wire        [31:0]          NPC_jump_Beq_offset;
    wire        [25:0]          NPC_jump_im_out;
    wire        [31:0]          NPC_jump_NPC_beq;        
    wire        [31:0]          NPC_jump_NPC_j;  
    //RegFile
    wire        [4:0]           RegFile_A1, RegFile_A2, RegFile_WBdst;
    wire        [31:0]          RegFile_WD;
    wire                        RegFile_RFWr;
    wire        [31:0]          RegFile_RD1, RegFile_RD2;
    //Ext
    wire        [15:0]          Ext_Imm16;
    wire        [1:0]           Ext_ExtOp;
    wire        [31:0]          Ext_Imm32;
    //Ctrl
	wire		[31:0]			Ctrl_instr;
	wire						Ctrl_EXE_stopThis;	//来自ID/EXE，确定是否废弃本条指令，即上条是否跳转成功
	wire		[4:0]			Ctrl_EXE_WBdst;
	wire		[5:0]			Ctrl_EXE_instrOp;
	wire						Ctrl_EXE_RegW;
	wire		[4:0]			Ctrl_MEM_WBdst;
	wire		[5:0]			Ctrl_MEM_instrOp;
	wire						Ctrl_MEM_RegW;
	wire		[31:0]			Ctrl_RegFileA;		//本级rf输出
	wire		[31:0]			Ctrl_RegFileB;
	wire 		[5:0]			Ctrl_instrOp;		//本条指令Op，传给ID_EXE
	wire 					    Ctrl_RegW;			//寄存器堆写入数据，为1写，否则不写
	wire					    Ctrl_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
	wire	    [1:0] 			Ctrl_NPCOp;			//00取PC+4，01取jump指令，10取beq指令
	wire					    Ctrl_MemW;			//写数据存储器	
	wire	    [1:0]			Ctrl_AluAsrc;		//Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
	wire	    [1:0]			Ctrl_AluBsrc;		//运算器操作数选择,00使用RegFileB,01使用立即数,10使用EXE级Alu_C，11使用MEM级结果
	wire	    [1:0] 			Ctrl_ExtOp;			//位扩展/符号扩展选择
	wire	    [3:0] 			Ctrl_Aluctrl;		//Alu运算选择
	wire					    Ctrl_stopNext;		//是否废弃下一条指令
	wire 		[4:0]			Ctrl_WBdst;			//目标寄存器，传给ID_EXE
	wire					    Ctrl_IF_IDWr;		//IF/ID寄存器写使能
	wire					    Ctrl_PCWr;			//PC写使能
    wire        [31:0]          Ctrl_MEM_out;
    wire        [31:0]          Ctrl_EXE_Alu_C;
    wire        [31:0]          Ctrl_MEM_Alu_C;
    wire                        Ctrl_MEM_WBsrc;
    wire                        Ctrl_MEMW_src;
    //regID_EXE_
    wire                        ID_EXE_ID_RegW;			//寄存器堆写入数据，为1写，否则不写
    wire                        ID_EXE_ID_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
    wire                        ID_EXE_ID_MemW;			//写数据存储器	
    wire        [1:0]           ID_EXE_ID_AluAsrc;		    //Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
    wire        [1:0]		    ID_EXE_ID_AluBsrc;		    //运算器操作数选择
    wire        [3:0] 		    ID_EXE_ID_Aluctrl;		    //Alu运算选择
    wire                        ID_EXE_ID_stopNext;		//是否废弃下一条指令
    wire        [4:0]	        ID_EXE_ID_WBdst;			//目标寄存器，传给ID_EXE
    wire        [5:0]		    ID_EXE_ID_instrOp;		    //本条指令Op，传给ID_EXE
    wire        [31:0]          ID_EXE_ID_RegFileA;
    wire        [31:0]          ID_EXE_ID_RegFileB;
    wire        [31:0]          ID_EXE_ID_Imm32; 
    wire                        ID_EXE_ID_MEMW_src;
    wire                        ID_EXE_EXE_RegW;			//寄存器堆写入数据，为1写，否则不写
    wire                        ID_EXE_EXE_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
    wire                        ID_EXE_EXE_MemW;			//写数据存储器	
    wire        [1:0]           ID_EXE_EXE_AluAsrc;		//Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
    wire        [1:0]		    ID_EXE_EXE_AluBsrc;		//运算器操作数选择
    wire        [3:0] 		    ID_EXE_EXE_Aluctrl;		//Alu运算选择
    wire                        ID_EXE_EXE_stopNext;		//是否废弃下一条指令
    wire        [4:0]	        ID_EXE_EXE_WBdst;			//目标寄存器，传给EXE_EXE
    wire        [5:0]		    ID_EXE_EXE_instrOp;		//本条指令Op，传给EXE_EXE
    wire        [31:0]          ID_EXE_EXE_RegFileA;
    wire        [31:0]          ID_EXE_EXE_RegFileB;
    wire        [31:0]          ID_EXE_EXE_Imm32; 
    wire                        EXE_MEMW_src;
//EXE
    //Alu_
    wire        [31:0]          Alu_A, Alu_B;
    wire        [3:0]           Alu_ALUOp;
    wire        [31:0]          Alu_C;
    //AluA_src
    wire        [31:0]          AluA_src_RegFileA;
    wire        [31:0]          AluA_src_EXE_AluC;
    wire        [31:0]          AluA_src_MEM_WriteData;
    wire        [1:0]           AluA_src_AluAsrc;
    wire        [31:0]          AluA_src_AluA;
    //AluB_src_
    wire        [31:0]          AluB_src_RegFileB;
    wire        [31:0]          AluB_src_EXT_Imm32;
    wire        [31:0]          AluB_src_EXE_AluC;
    wire        [31:0]          AluB_src_MEM_WriteData;
    wire        [1:0]           AluB_src_AluBsrc;
    wire        [31:0]          AluB_src_AluB;
    //regEXE_MEM_
    wire                        EXE_MEM_EXE_RegW;			//寄存器堆写入数据，为1写，否则不写
    wire                        EXE_MEM_EXE_RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
    wire                        EXE_MEM_EXE_MemW;			//写数据存储器	
    wire        [4:0]	        EXE_MEM_EXE_WBdst;			//目标寄存器
    wire        [5:0]		    EXE_MEM_EXE_instrOp;		//本条指令Op
    wire        [31:0]          EXE_MEM_EXE_Alu_C;
    wire        [31:0]          EXE_MEM_EXE_RegFileB;
    wire        [31:0]          EXE_MEM_EXE_RegFileA;
    wire                        EXE_MEM_EXE_MEMW_src;
    wire        [31:0]          EXE_MEM_MEM_RegFileA;
    wire                        EXE_MEM_MEM_RegW;
    wire                        EXE_MEM_MEM_RegW_Src;
    wire                        EXE_MEM_MEM_MemW;
    wire        [4:0]	        EXE_MEM_MEM_WBdst;
    wire        [5:0]		    EXE_MEM_MEM_instrOp;
    wire        [31:0]          EXE_MEM_MEM_Alu_C;
    wire        [31:0]          EXE_MEM_MEM_RegFileB;
    wire                        EXE_MEM_MEM_MEMW_src;
//MEM
    //DataMem
    wire        [9:0]           DM_addr;
    wire        [31:0]          DM_din;
    wire                        DM_DMWr;
    wire        [31:0]          DM_dout;
    wire                        DM_MEMW_src;
    wire        [31:0]          DM_WB_data;
    //regMEM_WB_
    wire        [31:0]          MEM_WB_MEM_DataMem;
    wire                        MEM_WB_MEM_RegW;
    wire                        MEM_WB_MEM_Reg_Src;
    wire        [4:0]           MEM_WB_MEM_WBdst;
    wire        [31:0]          MEM_WB_MEM_Alu_C;
    wire        [31:0]          MEM_WB_WB_DataMem;
    wire                        MEM_WB_WB_RegW;
    wire                        MEM_WB_WB_Reg_Src;
    wire        [4:0]           MEM_WB_WB_WBdst;
    wire        [31:0]          MEM_WB_WB_Alu_C;
//WB_
    wire        [31:0]          WB_Alu_C;
    wire        [31:0]          WB_MemRead;
    wire                        WB_RegW_Src;
    wire        [31:0]          WB_WriteData;
//初始化
    //IF
    InsMem U_InsMem( 
        .addr(IM_addr),
        .dout(IM_dout)
    );
    PC U_PC( 
        .clk(clk),
        .rst(rst),
        .PCWr(PC_PCWr),
        .NPC(PC_NPC),
        .PC(PC_PC)
    ); 
    NPC U_NPC(
        .NPC_4(NPC_NPC_4) , 
        .NPC_j(NPC_NPC_j) ,
        .NPC_beq(NPC_NPC_beq) ,
        .NPCOp(NPC_NPCOp) ,
        .NPC(NPC_NPC)
    );
    regIF_ID U_regIF_ID(
        .clk(clk) ,
        .rst(rst) ,
        .im_out(IF_ID_im_out) ,
        .PC(IF_ID_PC) ,
        .IF_im_out(IF_ID_IF_im_out) ,
        .IF_PC(IF_ID_IF_PC),
        .IF_IDWr(IF_ID_IF_IDWr)
    );
    //ID
    NPC_jump U_NPC_jump(
        .PC(NPC_jump_PC) ,
        .Beq_offset(NPC_jump_Beq_offset) ,
        .im_out(NPC_jump_im_out) ,
        .NPC_beq(NPC_jump_NPC_beq) ,
        .NPC_j(NPC_jump_NPC_j)
    );
    RegFile U_RegFile(
         .A1(RegFile_A1) ,
         .A2(RegFile_A2) ,
         .WBdst(RegFile_WBdst) ,
         .WD(RegFile_WD) ,
         .RFWr(RegFile_RFWr) ,
         .RD1(RegFile_RD1) ,
         .RD2(RegFile_RD2) 
    ); 
    Ext U_Ext(
        .Imm16(Ext_Imm16),
        .ExtOp(Ext_ExtOp),
        .Imm32(Ext_Imm32)
    );

    Ctrl U_Ctrl(
        .instr(Ctrl_instr) , 
        .EXE_stopThis(Ctrl_EXE_stopThis),
        .EXE_WBdst(Ctrl_EXE_WBdst) , 
        .EXE_instrOp(Ctrl_EXE_instrOp) ,
		.EXE_RegW(Ctrl_EXE_RegW) , 
        .MEM_WBdst(Ctrl_MEM_WBdst) , 
        .MEM_instrOp(Ctrl_MEM_instrOp) , 
        .MEM_RegW(Ctrl_MEM_RegW),
		.RegFileA(Ctrl_RegFileA) , 
        .RegFileB(Ctrl_RegFileB) , 
        .instrOp(Ctrl_instrOp) , 
        .RegW(Ctrl_RegW) , 
		.RegW_Src(Ctrl_RegW_Src) , 
        .NPCOp(Ctrl_NPCOp) , 
        .MemW(Ctrl_MemW) , 
        .AluAsrc(Ctrl_AluAsrc) , 
        .AluBsrc(Ctrl_AluBsrc) ,
		.ExtOp(Ctrl_ExtOp) , 
        .Aluctrl(Ctrl_Aluctrl) , 
        .stopNext(Ctrl_stopNext) , 
        .WBdst(Ctrl_WBdst) , 
        .IF_IDWr(Ctrl_IF_IDWr) , 
        .PCWr(Ctrl_PCWr),
        .MEM_out(Ctrl_MEM_out),
        .EXE_Alu_C(Ctrl_EXE_Alu_C),
        .MEM_Alu_C(Ctrl_MEM_Alu_C),
        .MEM_WBsrc(Ctrl_MEM_WBsrc),
        .MEMW_src(Ctrl_MEMW_src)
    );

    regID_EXE U_regID_EXE(
        .ID_RegW(ID_EXE_ID_RegW) ,
        .ID_RegW_Src(ID_EXE_ID_RegW_Src) , 
        .ID_MemW(ID_EXE_ID_MemW) , 	
        .ID_AluAsrc(ID_EXE_ID_AluAsrc) , 	
        .ID_AluBsrc(ID_EXE_ID_AluBsrc) , 
        .ID_Aluctrl(ID_EXE_ID_Aluctrl) , 
        .ID_stopNext(ID_EXE_ID_stopNext) , 
        .ID_WBdst(ID_EXE_ID_WBdst) , 			
        .ID_instrOp(ID_EXE_ID_instrOp) , 
        .ID_RegFileA(ID_EXE_ID_RegFileA) , 
        .ID_RegFileB(ID_EXE_ID_RegFileB) , 
        .ID_Imm32(ID_EXE_ID_Imm32),
        .ID_MEMW_src(ID_EXE_ID_MEMW_src),
        .clk(clk), 
        .rst(rst),
        .EXE_RegW(ID_EXE_EXE_RegW) , 
        .EXE_RegW_Src(ID_EXE_EXE_RegW_Src) , 
        .EXE_MemW(ID_EXE_EXE_MemW) , 
        .EXE_AluAsrc(ID_EXE_EXE_AluAsrc) , 	
        .EXE_AluBsrc(ID_EXE_EXE_AluBsrc) , 
        .EXE_Aluctrl(ID_EXE_EXE_Aluctrl) , 
        .EXE_stopNext(ID_EXE_EXE_stopNext) , 
        .EXE_WBdst(ID_EXE_EXE_WBdst) , 			
        .EXE_instrOp(ID_EXE_EXE_instrOp) , 
        .EXE_RegFileA(ID_EXE_EXE_RegFileA) , 
        .EXE_RegFileB(ID_EXE_EXE_RegFileB) , 
        .EXE_Imm32(ID_EXE_EXE_Imm32),
        .EXE_MEMW_src(ID_EXE_EXE_MEMW_src)
    );
    //EXE
    Alu U_Alu(
        .A(Alu_A), 
        .B(Alu_B), 
        .ALUOp(Alu_ALUOp) , 
        .C(Alu_C)
    ); 
    AluA_src U_AluA_src(
        .RegFileA(AluA_src_RegFileA) , 
        .EXE_AluC(AluA_src_EXE_AluC) , 
        .MEM_WriteData(AluA_src_MEM_WriteData) , 
        .AluAsrc(AluA_src_AluAsrc) , 
        .AluA(AluA_src_AluA)
    );
    AluB_src U_AluB_src(
        .RegFileB(AluB_src_RegFileB) , 
        .EXT_Imm32(AluB_src_EXT_Imm32),
        .EXE_AluC(AluB_src_EXE_AluC) , 
        .MEM_WriteData(AluB_src_MEM_WriteData) , 
        .AluBsrc(AluB_src_AluBsrc) , 
        .AluB(AluB_src_AluB)
    );
    regEXE_MEM U_regEXE_MEM(
        .MEM_RegW(EXE_MEM_MEM_RegW) , 
        .MEM_RegW_Src(EXE_MEM_MEM_RegW_Src) , 
        .MEM_MemW(EXE_MEM_MEM_MemW) , 
        .MEM_WBdst(EXE_MEM_MEM_WBdst), 
        .MEM_instrOp(EXE_MEM_MEM_instrOp) , 
        .EXE_RegFileB(EXE_MEM_EXE_RegFileB),
        .MEM_MEMW_src(EXE_MEM_MEM_MEMW_src),
        .clk(clk) , 
        .rst(rst) , 
        .EXE_RegW(EXE_MEM_EXE_RegW) , 
        .EXE_RegW_Src(EXE_MEM_EXE_RegW_Src),
        .EXE_Alu_C(EXE_MEM_EXE_Alu_C),
        .EXE_MemW(EXE_MEM_EXE_MemW) , 
        .MEM_Alu_C(EXE_MEM_MEM_Alu_C),
        .EXE_WBdst(EXE_MEM_EXE_WBdst) , 
        .EXE_instrOp(EXE_MEM_EXE_instrOp),
        .MEM_RegFileB(EXE_MEM_MEM_RegFileB),
        .EXE_MEMW_src(EXE_MEM_EXE_MEMW_src)
    );
    //MEM
    DataMem U_DataMem( 
        .addr(DM_addr), 
        .din(DM_din), 
        .DMWr(DM_DMWr), 
        .dout(DM_dout) ,
        .MEMW_src(DM_MEMW_src),
        .WB_data(DM_WB_data)
    );
    regMEM_WB U_regMEM_WB(
        .MEM_DataMem(MEM_WB_MEM_DataMem) ,
        .MEM_RegW(MEM_WB_MEM_RegW) , 
        .rst(rst) ,
        .MEM_Reg_Src(MEM_WB_MEM_Reg_Src) ,
        .MEM_WBdst(MEM_WB_MEM_WBdst) ,
        .MEM_Alu_C(MEM_WB_MEM_Alu_C) ,
        .clk(clk) ,
        .WB_DataMem(MEM_WB_WB_DataMem) ,
        .WB_RegW(MEM_WB_WB_RegW) ,
        .WB_Reg_Src(MEM_WB_WB_Reg_Src) ,
        .WB_WBdst(MEM_WB_WB_WBdst) ,
        .WB_Alu_C(MEM_WB_WB_Alu_C) 
    );
    //WB
    ChoseDataWrite U_ChoseDataWrite(
        .Alu_C(WB_Alu_C) ,
        .MemRead(WB_MemRead) ,
        .RegW_Src(WB_RegW_Src) ,
        .clk(clk),
        .WriteData(WB_WriteData)
    );
//IF连线
    assign IM_addr = PC_PC[11:2];

    assign PC_PCWr = Ctrl_PCWr;
    assign PC_NPC = NPC_NPC;

    assign NPC_NPC_4 = PC_PC + 3'b100;
    assign NPC_NPC_j = NPC_jump_NPC_j;
    assign NPC_NPC_beq = NPC_jump_NPC_beq;
    assign NPC_NPCOp = Ctrl_NPCOp;

    assign IF_ID_im_out = IM_dout;
    assign IF_ID_PC = PC_PC;

//ID连线
    assign NPC_jump_PC = IF_ID_IF_PC;
    assign NPC_jump_Beq_offset = Ext_Imm32;
    assign NPC_jump_im_out = IF_ID_IF_im_out;
    assign IF_ID_IF_IDWr = Ctrl_IF_IDWr;

    assign RegFile_A1 = IF_ID_IF_im_out [25:21];
    assign RegFile_A2 = IF_ID_IF_im_out [20:16];
    assign RegFile_WBdst = MEM_WB_WB_WBdst;
    assign RegFile_RFWr = MEM_WB_WB_RegW;
    assign RegFile_WD = WB_WriteData;

    assign Ext_Imm16 = IF_ID_IF_im_out;
    assign Ext_ExtOp = Ctrl_ExtOp;

    assign Ctrl_instr = IF_ID_IF_im_out;
    assign Ctrl_EXE_stopThis = ID_EXE_EXE_stopNext;
    assign Ctrl_EXE_WBdst = ID_EXE_EXE_WBdst;
    assign Ctrl_EXE_instrOp = ID_EXE_EXE_instrOp;
    assign Ctrl_EXE_instrOp = ID_EXE_EXE_instrOp;
    assign Ctrl_MEM_WBdst = EXE_MEM_MEM_WBdst;
    assign Ctrl_MEM_instrOp = EXE_MEM_MEM_instrOp;
    assign Ctrl_MEM_RegW = EXE_MEM_MEM_RegW;
    assign Ctrl_RegFileA = RegFile_RD1;
    assign Ctrl_RegFileB = RegFile_RD2;
    assign Ctrl_EXE_RegW = ID_EXE_EXE_RegW;
    assign Ctrl_MEM_out = DM_dout;
    assign Ctrl_MEM_Alu_C = EXE_MEM_MEM_Alu_C;
    assign Ctrl_MEM_WBsrc = EXE_MEM_MEM_WBdst;
    assign Ctrl_EXE_Alu_C = Alu_C;

    assign ID_EXE_ID_RegW = Ctrl_RegW;
    assign ID_EXE_ID_RegW_Src = Ctrl_RegW_Src;
    assign ID_EXE_ID_MemW = Ctrl_MemW;
    assign ID_EXE_ID_AluAsrc = Ctrl_AluAsrc;
    assign ID_EXE_ID_AluBsrc = Ctrl_AluBsrc;
    assign ID_EXE_ID_Aluctrl = Ctrl_Aluctrl;
    assign ID_EXE_ID_stopNext = Ctrl_stopNext;
    assign ID_EXE_ID_WBdst = Ctrl_WBdst;
    assign ID_EXE_ID_instrOp = Ctrl_instrOp;
    assign ID_EXE_ID_RegFileA = RegFile_RD1;
    assign ID_EXE_ID_RegFileB = RegFile_RD2;
    assign ID_EXE_ID_Imm32 = Ext_Imm32;
    assign ID_EXE_ID_MEMW_src = Ctrl_MEMW_src;

//EXE连线
    assign Alu_A = AluA_src_AluA;
    assign Alu_B = AluB_src_AluB;
    assign Alu_ALUOp = ID_EXE_EXE_Aluctrl;
    
    assign AluA_src_RegFileA = ID_EXE_EXE_RegFileA;
    assign AluA_src_EXE_AluC = EXE_MEM_MEM_Alu_C;
    assign AluA_src_MEM_WriteData = WB_WriteData;
    assign AluA_src_AluAsrc = ID_EXE_EXE_AluAsrc;

    assign AluB_src_RegFileB = ID_EXE_EXE_RegFileB;
    assign AluB_src_EXT_Imm32 = ID_EXE_EXE_Imm32;
    assign AluB_src_EXE_AluC = EXE_MEM_MEM_Alu_C;
    assign AluB_src_MEM_WriteData = WB_WriteData;
    assign AluB_src_AluBsrc = ID_EXE_EXE_AluBsrc;

    assign EXE_MEM_EXE_RegW = ID_EXE_EXE_RegW;
    assign EXE_MEM_EXE_RegW_Src = ID_EXE_EXE_RegW_Src;
    assign EXE_MEM_EXE_MemW = ID_EXE_EXE_MemW;
    assign EXE_MEM_EXE_instrOp = ID_EXE_EXE_MemW;
    assign EXE_MEM_EXE_Alu_C = Alu_C;
    assign EXE_MEM_EXE_RegFileB = ID_EXE_EXE_RegFileB;
    assign EXE_MEM_EXE_WBdst = ID_EXE_EXE_WBdst;
    assign EXE_MEM_EXE_RegFileA = ID_EXE_EXE_RegFileA;
    assign EXE_MEM_EXE_MEMW_src = ID_EXE_EXE_MEMW_src;

//MEM连线
    assign DM_addr = EXE_MEM_MEM_Alu_C[11:2];
    assign DM_din = EXE_MEM_MEM_RegFileB;
    assign DM_DMWr = EXE_MEM_MEM_MemW;
    assign DM_MEMW_src = EXE_MEM_MEM_MEMW_src;
    assign DM_WB_data = WB_WriteData;

    assign MEM_WB_MEM_DataMem = DM_dout;
    assign MEM_WB_MEM_RegW = EXE_MEM_MEM_RegW;
    assign MEM_WB_MEM_Reg_Src = EXE_MEM_MEM_RegW_Src;
    assign MEM_WB_MEM_WBdst = EXE_MEM_MEM_WBdst;
    assign MEM_WB_MEM_Alu_C = EXE_MEM_MEM_Alu_C;
//WB连线
    assign WB_Alu_C = MEM_WB_WB_Alu_C;
    assign WB_MemRead = MEM_WB_WB_DataMem;
    assign WB_RegW_Src = MEM_WB_WB_Reg_Src;
endmodule