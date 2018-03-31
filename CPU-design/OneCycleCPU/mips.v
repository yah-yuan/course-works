module mips( clk, rst );
    input   clk;
    input   rst;
//InsMem in
    wire    [9:0]          im_addr;
//InsMem out
    wire    [31:0]          im_dout;
    wire    [5:0]           im_Op;
    wire    [5:0]           im_Funct;
    wire    [4:0]           im_rs;
    wire    [4:0]           im_rt;
    wire    [4:0]           im_rd;
    wire    [15:0]          im_Imm16;
    wire    [25:0]          im_IMM;     //NPC
//PC in
    wire                    PC_Wr;
    wire    [31:0]          PC_NPC;
//PC out
    wire    [31:0]          PC_out;
//alu in
    wire    [31:0]          alu_A,alu_B;
    wire    [3:0]           alu_ALUop;
//alu out
    wire    [31:0]          alu_C;
    wire                    alu_Zero;
//DataRAM in
    wire    [11:2]          dm_addr;
    wire    [31:0]          dm_din;
    wire 		            dm_DMWr;
//DataRAM out
    wire    [31:0]          dm_dout;
//EXT in
    wire    [15:0]          EXT_Imm16;
    wire    [1:0]           EXT_EXTop;   //ext使能
//EXT out
    wire    [31:0]          EXT_Imm32;
//Ctrl in
    wire    [5:0]           Ctrl_OpCode;
    wire    [5:0]           Ctrl_funct;
//Ctrl out
    wire                    Ctrl_RegDst;
    wire                    Ctrl_MemR;
    wire                    Ctrl_Mem2R;
    wire                    Ctrl_MemW;
    wire                    Ctrl_RegW;
    wire                    Ctrl_Alusrc;
    wire    [1:0]           Ctrl_ExtOp;
    wire    [3:0]           Ctrl_Aluctrl;  
    wire    [1:0]           Ctrl_NPCop;
//RF in
    wire    [4:0]           RF_A1, RF_A2, RF_A3;
    wire    [31:0]          RF_WD;
    wire                    RF_RFWr;
    wire                    RF_RegDst;
//RF out
    wire    [31:0]          RF_RD1, RF_RD2;
//NPC in
    wire    [31:0]          NPC_PC;
    wire                    NPC_alu_zero;
    wire    [1:0]           NPC_NPCop;
    wire    [31:0]          NPC_Beq_offset;
    wire    [25:0]          NPC_im_out;
//NPC out
    wire    [31:0]          NPC_NPC;
//Mux2 alu_b_select in
    wire    [31:0]          Mux2_aluB_d0;
    wire    [31:0]          Mux2_aluB_d1;
    wire                    Mux2_aluB_s;
//Mux2 alu_b_select out
    wire    [31:0]          Mux2_aluB_y;
//Mux2 alu_out and mem_out 2 to 1 in
    wire    [31:0]          Mux2_mem2r_d0;
    wire    [31:0]          Mux2_mem2r_d1;
    wire                    Mux2_mem2r_s;
//Mux2 alu_out and mem_out 2 to 1 out
    wire    [31:0]          Mux2_mem2r_y;
//im实例化
    im_4k U_im_4k(
        .addr(im_addr),
        .dout(im_dout)
    );
    assign  im_Op = im_dout[31:26];
    assign  im_Funct = im_dout[5:0];
    assign  im_rs = im_dout[25:21];
    assign  im_rt = im_dout[20:16];
    assign  im_rd = im_dout[15:11];
    assign  im_Imm16 = im_dout[15:0];
    assign  im_IMM = im_dout[25:0];  
//PC实例化
    PC U_PC (
        .clk(clk), 
        .rst(rst),
        .PCWr(PC_Wr), 
        .NPC(PC_NPC), 
        .PC(PC_out)
   ); 
//Alu实例化
    alu U_alu(
        .A(alu_A),
        .B(alu_B),
        .ALUOp(alu_ALUop),
        .C(alu_C),
        .Zero(alu_Zero)
    );
//dm实例化
    dm_4k U_dm_4k(
        .addr(dm_addr),
        .din(dm_din),
        .DMWr(dm_DMWr),
        .clk(clk),
        .dout(dm_dout)
    );
//EXT实例化
    EXT U_EXT(
        .Imm16(EXT_Imm16),
        .EXTOp(EXT_EXTop),
        .Imm32(EXT_Imm32)
    );
//Ctrl实例化
    Ctrl U_Ctrl(
        .OpCode(Ctrl_OpCode),
        .funct(Ctrl_funct),
        .RegDst(Ctrl_RegDst),
        .NPCop(Ctrl_NPCop),
        .MemR(Ctrl_MemR),
        .Mem2R(Ctrl_Mem2R),
        .MemW(Ctrl_MemW),
        .RegW(Ctrl_RegW),
        .Alusrc(Ctrl_Alusrc),
        .ExtOp(Ctrl_ExtOp),
        .Aluctrl(Ctrl_Aluctrl)
    );
//RF实例化
    RF U_RF(
        .A1(RF_A1),
        .A2(RF_A2),
        .A3(RF_A3),
        .WD(RF_WD),
        .clk(clk),
        .RFWr(RF_RFWr),
        .RD1(RF_RD1),
        .RD2(RF_RD2),
        .RegDst(RF_RegDst)
    );

//NPC实例化
    NPC U_NPC(
        .PC(NPC_PC), 
        .NPC(NPC_NPC),
        .Beq_offset(NPC_Beq_offset),
        .alu_zero(NPC_alu_zero),
        .NPCop(NPC_NPCop),
        .im_out(NPC_im_out)
    );

//Mux实例化
    //alu B 2选1
    mux2 U_Mux2_aluB(
        .d0(Mux2_aluB_d0),
        .d1(Mux2_aluB_d1),
        .s(Mux2_aluB_s),
        .y(Mux2_aluB_y)
    );
    //alu_out and mem_out 2 to 1
    mux2 U_Mux2_mem2r(
        .d0(Mux2_mem2r_d0),
        .d1(Mux2_mem2r_d1),
        .s(Mux2_mem2r_s),
        .y(Mux2_mem2r_y)
    );

//连线
    //Ctrl in
    assign Ctrl_OpCode = im_Op;
    assign Ctrl_funct = im_Funct;
    //EXT in
    assign EXT_Imm16 = im_Imm16;
    assign EXT_EXTop = Ctrl_ExtOp;
    //NPC in
    assign NPC_PC = PC_out;
    assign NPC_NPCop = Ctrl_NPCop;
    assign NPC_Beq_offset = EXT_Imm32;
    assign NPC_alu_zero = alu_Zero;
    assign NPC_im_out = im_IMM;
    //PC in
    assign PC_NPC = NPC_NPC;
    assign PC_Wr = 1'b1;
    //alu in
    assign alu_ALUop = Ctrl_Aluctrl;
    assign alu_A = RF_RD1;
    assign alu_B = Mux2_aluB_y;
    //RF in
    assign RF_A1 = im_rs;
    assign RF_A2 = im_rt;
    assign RF_A3 = im_rd;
    assign RF_WD = Mux2_mem2r_y;
    assign RF_RFWr = Ctrl_RegW;
    assign RF_RegDst = Ctrl_RegDst;
    //dm in
    assign dm_addr = alu_C[11:2];
    assign dm_din = RF_RD2;
    assign dm_DMWr = Ctrl_MemW;
    //im in
    assign im_addr = PC_out[11:2];
    //alu B 2选1 in
    assign Mux2_aluB_d0 = RF_RD2;
    assign Mux2_aluB_d1 = EXT_Imm32;
    assign Mux2_aluB_s = Ctrl_Alusrc;
    //alu_out and mem_out 2 to 1
    assign Mux2_mem2r_d0 = alu_C;
    assign Mux2_mem2r_d1 = dm_dout;
    assign Mux2_mem2r_s = Ctrl_Mem2R;
endmodule