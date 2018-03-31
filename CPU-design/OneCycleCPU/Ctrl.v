

module Ctrl(RegDst,MemR,Mem2R,MemW,RegW,Alusrc,ExtOp,Aluctrl,funct,OpCode,NPCop);
	
	input [5:0]		OpCode;				//指令功能字段
	input [5:0]		funct;				//指令操作码字段

	output RegW;						//寄存器堆写入数据，为1写，否则不写
	output RegDst;						//目标寄存器号，为1选择rt，否则rd
	output Mem2R;						//数据存储器到寄存器堆，1写入，否则不写
	output wire[1:0] NPCop;
	output MemR;						//读存储器
	output MemW;						//写数据存储器
	
	output Alusrc;						//运算器操作数选择,1使用立即数
	output wire[1:0] ExtOp;				//位扩展/符号扩展选择
	output wire[3:0] Aluctrl;			//Alu运算选择

//指令解析
	wire r_type = ~OpCode[5] & ~OpCode[4] & ~OpCode[3] & ~OpCode[2] & ~OpCode[1] & ~OpCode[0];
	wire i_addu = r_type & funct[5] & ~funct[4] & ~funct[3] & ~funct[2] & ~funct[1] & funct[0];
	wire i_subu = r_type & funct[5] & ~funct[4] & ~funct[3] & ~funct[2] & funct[1] & funct[0];
	wire i_ori = ~OpCode[5] & ~OpCode[4] & OpCode[3] & OpCode[2] & ~OpCode[1] & OpCode[0];
	wire i_lw = OpCode[5] & ~OpCode[4] & ~OpCode[3] & ~OpCode[2] & OpCode[1] & OpCode[0];
	wire i_sw = OpCode[5] & ~OpCode[4] & OpCode[3] & ~OpCode[2] & OpCode[1] & OpCode[0];
	wire i_beq = ~OpCode[5] & ~OpCode[4] & ~OpCode[3] & OpCode[2] & ~OpCode[1] & ~OpCode[0];
	wire i_j = ~OpCode[5] & ~OpCode[4] & ~OpCode[3] & ~OpCode[2] & OpCode[1] & ~OpCode[0];
	wire i_lui = ~OpCode[5] & ~OpCode[4] & OpCode[3] & OpCode[2] & OpCode[1] & OpCode[0];
//op赋值
	assign RegW	= i_addu | i_subu | i_ori | i_lw | i_lui | 1'b0;
	assign RegDst = i_ori | i_lw | i_lui | 1'b0;
	assign jump = i_j | 1'b0;
	assign Mem2R = i_lw | 1'b0;
	assign Branch = i_beq | 1'b0;
	assign MemR = i_lw | 1'b0;
	assign MemW = i_sw | 1'b0;
	assign Alusrc =i_ori | i_lw | i_sw | i_lui | 1'b0;
	assign ExtOp[1] = i_lui | 1'b0;
	assign ExtOp[0] = i_beq | 1'b0;
	assign Aluctrl[3] = 1'b0;
	assign Aluctrl[2] = i_ori | i_subu | 1'b0;
	assign Aluctrl[1] = 1'b0;
	assign Aluctrl[0] = i_ori | 1'b0;
	assign NPCop[1] = i_beq | 1'b0;
	assign NPCop[0] = i_j |1'b0;

endmodule