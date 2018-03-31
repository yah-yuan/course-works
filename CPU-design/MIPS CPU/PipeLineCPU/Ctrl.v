//指令解析
	`define 	SW_OP         	6'b101011
	`define 	LW_OP         	6'b100011
	`define 	ORI_OP        	6'b001101 
	`define 	LUI_OP        	6'b001111
	`define 	BEQ_OP        	6'b000100
	`define 	J_OP          	6'b000010
	`define 	ADDU_OP    		6'b100001
	`define 	SUBU_OP    		6'b100011
module Ctrl( instr ,EXE_stopThis , EXE_WBdst , EXE_instrOp ,
			EXE_RegW , MEM_WBdst , MEM_instrOp , MEM_RegW,
			RegFileA , RegFileB , instrOp , RegW , 
			RegW_Src , NPCOp , MemW , AluAsrc , AluBsrc ,
			ExtOp , Aluctrl , stopNext , WBdst , IF_IDWr , PCWr,
			MEM_out ,EXE_Alu_C , MEM_Alu_C ,MEM_WBsrc,MEMW_src);
	
	input		[31:0]			instr;
	input						EXE_stopThis;	//来自ID/EXE，确定是否废弃本条指令，即上条是否跳转成功
	input		[4:0]			EXE_WBdst;
	input		[5:0]			EXE_instrOp;
	input						EXE_RegW;
	input		[4:0]			MEM_WBdst;
	input		[5:0]			MEM_instrOp;
	input						MEM_RegW;
	input		[31:0]			RegFileA;		//本级rf输出
	input		[31:0]			RegFileB;
	input		[31:0]			MEM_out;
	input		[31:0]			EXE_Alu_C;
	input		[31:0]			MEM_Alu_C;
	input						MEM_WBsrc;

//指令分解
	output 		[5:0]			instrOp;		//本条指令Op，传给ID_EXE
	wire		[4:0]			instrRs;
	wire		[4:0]			instrRt;
	wire		[4:0]			instrRd;
	wire		[5:0]			instrFunct;
//op信号量
	output reg					RegW;			//寄存器堆写入数据，为1写，否则不写
	output reg					RegW_Src;		//写入寄存器堆数据选择，1写入Mem读数，否则Alu结果
	output reg	[1:0] 			NPCOp;			//00取PC+4，01取jump指令，10取beq指令
	output reg					MemW;			//写数据存储器	
	output reg	[1:0]			AluAsrc;		//Alu_A的选择，00选择RegFileA,01选择EXE级Alu_C，10选择MEM级结果
	output reg	[1:0]			AluBsrc;		//运算器操作数选择,00使用RegFileB,01使用立即数,10使用EXE级Alu_C，11使用MEM级结果
	output reg	[1:0] 			ExtOp;			//位扩展/符号扩展选择
	output reg	[3:0] 			Aluctrl;		//Alu运算选择
	output reg					stopNext;		//是否废弃下一条指令
	output 		[4:0]			WBdst;			//目标寄存器，传给ID_EXE
	output reg					IF_IDWr;		//IF/ID寄存器写使能
	output reg					MEMW_src;		//1选wb级写回数据
	output reg					PCWr;			//PC写使能
	reg							RegWDst;		//写目标寄存器号，为1选择rd，0为rt
	reg	  		[31:0]			Num1;
	reg  		[31:0]			Num2;			//用于beq检测
//分量赋值
	assign instrOp = instr[31:26]; 
	assign instrRs = instr[25:21];
	assign instrRt = instr[20:16];
	assign instrRd = instr[15:11];
	assign instrFunct = instr[5:0];
	assign WBdst = RegWDst ? instrRd : instrRt;

	initial
	begin
		RegW = 0;								//寄存器不可写
		RegW_Src = 0;							//从Alu写入寄存器，而非MEM
		NPCOp = 2'b00;							//取PC+4作为下条指令
		MemW = 0;								//RAM不可写
		AluAsrc = 2'b00;						//AluB数据源为RegFileB
		AluBsrc = 2'b00;						//AluA数据源为RegFileA
		ExtOp = 2'b00;							//正常扩展
		Aluctrl = 4'b0000;						//使用加法计算
		stopNext = 0;							//下条不废弃
		IF_IDWr = 1;							//IF/ID可写
		PCWr = 1;								//PC可写
		RegWDst = 0;
		MEMW_src = 0;
	end
//op赋值
	always @( * )
	begin
	//初始化
		RegW = 0;								//寄存器不可写
		RegW_Src = 0;							//从Alu写入寄存器，而非MEM
		NPCOp = 2'b00;							//取PC+4作为下条指令
		MemW = 0;								//RAM不可写
		AluAsrc = 2'b00;						//AluB数据源为RegFileB
		AluBsrc = 2'b00;						//AluA数据源为RegFileA
		ExtOp = 2'b00;							//正常扩展
		Aluctrl = 4'b0000;						//使用加法计算
		stopNext = 0;							//下条不废弃
		IF_IDWr = 1;							//IF/ID可写
		PCWr = 1;								//PC可写

		case ( instrOp )
			6'b0:
			begin
				case (instrFunct)
					`ADDU_OP:
					begin
						RegW = 1;
						RegWDst = 1;
						Aluctrl = 4'b0000;
					end
					`SUBU_OP:
					begin
						RegW = 1;
						Aluctrl = 4'b0100;
						RegWDst = 1;
						Aluctrl = 4'b0100;
					end
				endcase
			end
			`LUI_OP:
			begin
				RegW = 1;
				RegWDst = 0;					//写到rt
				AluBsrc = 2'b01;				//来自EXT
				ExtOp = 2'b10;
			end
			`ORI_OP:
			begin
				RegW = 1;
				RegWDst = 0;
				AluBsrc = 2'b01;
				Aluctrl = 4'b0101;
			end
			`LW_OP:
			begin
				RegW = 1;
				RegWDst = 0;
				AluBsrc = 2'b01;
				RegW_Src = 1;
			end
			`SW_OP:
			begin
				MemW = 1;
				AluBsrc = 2'b01;
				RegWDst = 0;
				MEMW_src = 0;
			end
			`BEQ_OP: 
			begin
				if( MEM_RegW)
				begin
					if( instrRs == MEM_WBdst)
					begin
						Num1 = (MEM_WBsrc) ? MEM_out : MEM_Alu_C;
					end
					else
					begin
						Num1 = RegFileA;
					end
					if( instrRt == MEM_WBdst)
					begin
						Num2 = (MEM_WBsrc) ? MEM_out : MEM_Alu_C;
					end
					else
					begin
						Num2 = RegFileB;
					end
				end	
				if( EXE_RegW )
				begin
					Num1 = (instrRs == EXE_WBdst) ? EXE_Alu_C : RegFileA;
					Num2 = (instrRt == EXE_WBdst) ? EXE_Alu_C : RegFileB;
				end	
				if(Num1 == Num2)		//跳转
				begin
					stopNext = 1;
					NPCOp = 2'b10;
					ExtOp = 2'b01;
				end
				RegWDst = 0;
				MemW = 0;
			end
			`J_OP:
			begin
				stopNext = 1;
				NPCOp = 2'b01;
				RegWDst = 0;
				RegW = 0;
				MemW = 0;
			end
			default: $display("error!");
		endcase
//相关转发与阻塞
		if(EXE_stopThis)						//上条跳转
		begin
			RegW = 0;
			MemW = 0;
			NPCOp = 2'b0;
		end
		else 
		begin
			if(EXE_RegW)
			begin
				if(EXE_instrOp == `LW_OP)
				begin
					RegW = 0;
					MemW = 0;
					IF_IDWr = 0;
					PCWr = 0;
				end
				else if(instrOp == `SW_OP)
				begin
					if(instrRt == EXE_WBdst)
						begin
							MEMW_src = 1;
						end
				end
				else
				begin
					if( instrRs == EXE_WBdst )
					begin
						AluAsrc = 01;
					end
					else if(RegWDst)
					begin
						if(instrRt == EXE_WBdst)
						begin
							AluBsrc = 10;
						end
					end
				end
			end	
			if(MEM_RegW)
			begin
				if(instrRs == MEM_WBdst)
				begin
					AluAsrc = 2'b10;
				end
				else if(RegWDst)
				begin
					if(instrRt == MEM_WBdst)
					begin
						AluBsrc = 2'b11;
					end
				end
			end
		end
	end
//
endmodule