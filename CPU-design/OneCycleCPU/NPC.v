module NPC (PC ,NPC ,Beq_offset ,NPCop ,alu_zero ,im_out);
    input   [31:0]      PC;
    input   [31:0]      Beq_offset;
    input   [1:0]       NPCop;
    input               alu_zero;
    input   [25:0]      im_out;
    output  reg[31:0]   NPC;

    wire    [31:0]      NPC_4;        //00
    wire    [31:0]      NPC_beq;
    wire    [31:0]      NPC_j;
    wire    [31:0]      m_PC;
    wire    [31:0]      w_Beq_offset;
    wire    [1:0]       last_op;

    assign m_PC = PC + 3'b100;
    assign last_op[1] = NPCop[1] & alu_zero;
    assign last_op[0] = NPCop[0];
  
    assign NPC_j[31:28] = m_PC[31:28];
    assign NPC_j[27:2] = im_out;
    assign NPC_j[1:0] = 2'b00;

    assign w_Beq_offset[31:2] = Beq_offset[29:0];
    assign w_Beq_offset[1:0] = 2'b0;
    assign NPC_beq = m_PC + w_Beq_offset;

    assign NPC_4 = m_PC;

    always @( * ) begin
        case ( last_op )
            2'b00: NPC = NPC_4;
            2'b01: NPC = NPC_j;
            2'b10: NPC = NPC_beq;
            default: $display("NPCop error");
        endcase             
    end // end always

endmodule